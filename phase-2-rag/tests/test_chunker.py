import pytest
from ingestion.chunker import split_text
from pathlib import Path

def test_happy_path(chunker_config):    
    text = "paragraph one.\n\nparagraph two.\n\nparagraph three."
    chunks = split_text(text,chunker_config['chunk_size'],chunker_config['overlap_size'],chunker_config['separators'])    
    assert all(len(chunk) <=  (chunker_config['chunk_size'] + chunker_config['overlap_size']) for chunk in chunks)

def test_overlap(chunker_config):
    text = "paragraph one.\n\nparagraph two.\n\nparagraph three."
    chunks = split_text(text,chunker_config['chunk_size'],chunker_config['overlap_size'],chunker_config['separators'])        
    for i in range(len(chunks)):        
        if i == len(chunks)-1:
            break
        s = 0
        e = len(chunks[i]) - chunker_config['overlap_size']        
        previous_tail = chunks[i][e:]        
        e = chunker_config['overlap_size']
        current_starting = chunks[i+1][:e]                
        assert previous_tail==current_starting

def test_empty(chunker_config):
    text = ""
    chunks = split_text(text,chunker_config['chunk_size'],chunker_config['overlap_size'],chunker_config['separators'])            
    assert chunks == []

def test_short_text(chunker_config):
    text = "short text"
    chunks = split_text(text,chunker_config['chunk_size'],chunker_config['overlap_size'],chunker_config['separators'])            
    assert chunks == ['short text']
