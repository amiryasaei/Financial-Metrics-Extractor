"""
Results rendering components: tables, cards, and export functionality.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Tuple


def render_processing_summary(summary: Dict):
    """Render processing summary in an expander."""
    with st.expander('View Processing Summary'):
        st.write(f"**Total Files:** {summary['total_files']}")
        st.write(f"**Successful:** {summary['successful']}")
        st.write(f"**Failed:** {summary['failed']}")
        
        # Display processing time
        processing_time = summary.get('processing_time', 0.0)
        if processing_time > 0:
            if processing_time < 1:
                time_str = f"{processing_time * 1000:.0f} ms"
            elif processing_time < 60:
                time_str = f"{processing_time:.2f} seconds"
            else:
                minutes = int(processing_time // 60)
                seconds = processing_time % 60
                time_str = f"{minutes}m {seconds:.1f}s"
            st.write(f"**Processing Time:** {time_str}")


def create_results_dataframe(results: List[Tuple[str, Dict, str]]) -> pd.DataFrame:
    """
    Create a DataFrame from extraction results.
    
    Args:
        results: List of (filename, metrics_dict, error) tuples
        
    Returns:
        DataFrame: Formatted results table
    """
    rows = []
    for filename, metrics, error in results:
        row = {'company': filename.replace('.pdf', '').replace('_', ' ')}
        row.update(metrics)
        if error:
            row['error'] = error
        rows.append(row)
    
    return pd.DataFrame(rows)


def render_metric_cards(metrics: Dict, company: str):
    """Render metric values as cards."""
    st.subheader('**Extracted Metrics**')
    cols = st.columns(min(len(metrics), 4))
    
    for idx, (metric, value) in enumerate(metrics.items()):
        with cols[idx % len(cols)]:
            if value is not None:
                st.metric(label=metric.replace('_', ' ').title(), value=value)
            else:
                st.metric(label=metric.replace('_', ' ').title(), value='N/A')


def render_results_table(df: pd.DataFrame):
    """
    Render the results DataFrame as a table.
    
    Args:
        df: DataFrame to display
    """
    st.subheader('**Extraction Results**')
    st.dataframe(df, use_container_width=True)


def render_csv_export(df: pd.DataFrame):
    """Render CSV download button."""
    st.markdown('---')
    st.subheader('**Export Results**')
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label='Download CSV',
        data=csv,
        file_name='extraction_results.csv',
        mime='text/csv'
    )


def render_results(results: List[Tuple[str, Dict, str]]):
    """
    Main results rendering function.
    
    Args:
        results: List of (filename, metrics_dict, error) tuples
    """
    if not results:
        return
    
    # Get processing time from session state if available
    processing_time = st.session_state.processing_summary.get('processing_time', 0.0)
    
    summary = {
        'total_files': len(results),
        'successful': sum(1 for _, _, err in results if not err),
        'failed': sum(1 for _, _, err in results if err),
        'processing_time': processing_time
    }
    
    st.success(f"**Extraction Complete** - Processed {summary['successful']} successful of {summary['total_files']} total_files")
    
    render_processing_summary(summary)
    
    df = create_results_dataframe(results)
    render_results_table(df)
    render_csv_export(df)

