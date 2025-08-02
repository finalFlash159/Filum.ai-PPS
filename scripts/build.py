#!/usr/bin/env python3
"""
Build Embeddings Script for Filum.ai Knowledge Base
Run this script to pre-compute embeddings for all features
"""

import os
import sys
import logging
import argparse
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.embeddings import EmbeddingManager

def setup_logging(verbose: bool = False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('embedding_build.log')
        ]
    )

def check_dependencies():
    """Check if required dependencies are installed"""
    missing_deps = []
    
    try:
        import sentence_transformers
    except ImportError:
        missing_deps.append('sentence-transformers')
    
    try:
        import numpy
    except ImportError:
        missing_deps.append('numpy')
    
    if missing_deps:
        print(f"Missing dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install " + " ".join(missing_deps))
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Build embeddings for Filum.ai knowledge base')
    parser.add_argument(
        '--knowledge-base', 
        default='data/filum_knowledge_base.json',
        help='Path to knowledge base JSON file'
    )
    parser.add_argument(
        '--output', 
        default='data/filum_embeddings.pkl',
        help='Path to save embeddings cache'
    )
    parser.add_argument(
        '--force', 
        action='store_true',
        help='Force rebuild even if cache exists'
    )
    parser.add_argument(
        '--verbose', 
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Resolve paths
    knowledge_base_path = os.path.abspath(args.knowledge_base)
    output_path = os.path.abspath(args.output)
    
    logger.info("=== Filum.ai Embedding Builder ===")
    logger.info(f"Knowledge Base: {knowledge_base_path}")
    logger.info(f"Output Path: {output_path}")
    logger.info(f"Force Rebuild: {args.force}")
    
    # Check if knowledge base exists
    if not os.path.exists(knowledge_base_path):
        logger.error(f"Knowledge base not found: {knowledge_base_path}")
        sys.exit(1)
    
    # Check if output already exists
    if os.path.exists(output_path) and not args.force:
        logger.warning(f"Embeddings cache already exists: {output_path}")
        logger.warning("Use --force to rebuild or specify different --output path")
        
        # Ask user for confirmation
        response = input("Do you want to rebuild? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            logger.info("Aborted by user")
            sys.exit(0)
    
    try:
        # Create embedding manager
        manager = EmbeddingManager(knowledge_base_path, output_path)
        
        # Build embeddings
        logger.info("Starting embedding generation...")
        start_time = datetime.now()
        
        embeddings = manager.build_embeddings_from_knowledge_base()
        
        if not embeddings:
            logger.error("No embeddings were created")
            sys.exit(1)
        
        # Save embeddings
        logger.info("Saving embeddings...")
        if manager.save_embeddings(embeddings):
            logger.info("Embeddings saved successfully")
        else:
            logger.error("Failed to save embeddings")
            sys.exit(1)
        
        # Report statistics
        end_time = datetime.now()
        duration = end_time - start_time
        
        stats = manager.get_embedding_stats()
        
        logger.info("=== Build Complete ===")
        logger.info(f"Features processed: {stats['total_features']}")
        logger.info(f"Embedding dimension: {stats['embedding_dimension']}")
        logger.info(f"Build time: {duration.total_seconds():.2f} seconds")
        logger.info(f"Cache file: {stats['cache_file']}")
        
        print(f"\n✅ Successfully built embeddings for {stats['total_features']} features")
        print(f"📁 Saved to: {output_path}")
        print(f"⏱️  Build time: {duration.total_seconds():.2f} seconds")
        
    except KeyboardInterrupt:
        logger.info("Build interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Build failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
