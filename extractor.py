"""
PDF Metrics Extraction Module

This module handles PDF text extraction and LLM-based metrics extraction
with support for dynamic metrics and async parallel processing.
"""

import pdfplumber
import json
import re
import asyncio
from typing import Dict, Any, List, Tuple, Optional
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()


def extract_text_from_pdf(file) -> str:
    """
    Extract raw text from a PDF file using pdfplumber.

    Args:
        file: File-like object (from Streamlit uploader)
        
    Returns:
        str: Extracted text from all pages
    """
    text_parts = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
    return '\n\n'.join(text_parts)


def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text.

    Args:
        text: Raw extracted text from PDF
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extraction_prompt(text: str, metrics: List[str]) -> str:
    """
    Create a structured prompt for LLM-based metrics extraction.

    Args:
        text: Extracted text from PDF
        metrics: List of metric names to extract
        
    Returns:
        str: Formatted prompt for OpenAI
    """
    metrics_list = "\n".join([f"- {metric}: " for metric in metrics])
    
    prompt = f"""Extract the following financial metrics from the provided text. 
Return a JSON object with the metric names as keys and their values as numbers (in millions if applicable) or null if not found.

Metrics to extract:
{metrics_list}

Text:
{text[:8000]}

Return only valid JSON in this format:
{{
    "revenue": 123.5,
    "gross_margin": 45.2,
    ...
}}"""
    return prompt


def extract_with_llm(text: str, metrics: List[str]) -> Dict[str, Any]:
    """
    Send text to OpenAI LLM for metrics extraction.

    Args:
        text: Extracted text from PDF
        metrics: List of metric names to extract
        
    Returns:
        dict: Parsed JSON with metrics (or dict with all null on failure)
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return {metric: None for metric in metrics}
    
    client = OpenAI(api_key=api_key)
    
    prompt = extraction_prompt(text, metrics)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a financial data extraction assistant. Extract metrics and return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        
        content = response.choices[0].message.content.strip()
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = re.sub(r'^```(?:json)?\s*', '', content)
            content = re.sub(r'\s*```$', '', content)
        
        result = json.loads(content)
        # Ensure all requested metrics are in the result
        for metric in metrics:
            if metric not in result:
                result[metric] = None
        return result
    except Exception as e:
        print(f"LLM extraction error: {e}")
        return {metric: None for metric in metrics}


async def async_extract(text: str, filename: str, metrics: List[str]) -> Tuple[str, Dict[str, Any], Optional[str]]:
    """
    Async wrapper for LLM extraction with error handling.

    Args:
        text: Extracted text from PDF
        filename: Name of the file being processed
        metrics: List of metric names to extract
        
    Returns:
        tuple: (filename, result_dict, error_message)
    """
    try:
        # Run the synchronous extraction in executor
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, extract_with_llm, text, metrics)
        return (filename, result, None)
    except Exception as e:
        return (filename, {metric: None for metric in metrics}, str(e))


def process_all(files: List, metrics: List[str]) -> List[Tuple[str, Dict[str, Any], Optional[str]]]:
    """
    Process all PDF files in parallel using async extraction.

    Args:
        files: List of uploaded file objects
        metrics: List of metric names to extract
        
    Returns:
        list: List of tuples (filename, result_dict, error_message)
    """
    async def process_all_async():
        tasks = []
        for file in files:
            try:
                text = extract_text_from_pdf(file)
                cleaned = clean_text(text)
                task = async_extract(cleaned, file.name, metrics)
                tasks.append(task)
            except Exception as e:
                # Create a coroutine that returns error result
                async def error_result():
                    return (file.name, {metric: None for metric in metrics}, str(e))
                tasks.append(error_result())
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    
    # Try to get existing event loop, create new one if needed
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    try:
        results = loop.run_until_complete(process_all_async())
        return [r for r in results if not isinstance(r, Exception)]
    finally:
        if loop.is_running():
            loop.close()

