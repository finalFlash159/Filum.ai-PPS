"""
Embedding Manager for Filum.ai Knowledge Base
Pre-computes and manages embeddings for efficient matching
"""

import json
import pickle
import numpy as np
import logging
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class FeatureEmbedding:
    """Embedding data for a single feature"""
    feature_id: str
    description_embedding: np.ndarray
    pain_points_embedding: np.ndarray
    keywords_embedding: np.ndarray
    use_cases_embedding: np.ndarray
    combined_embedding: np.ndarray
    metadata: Dict[str, Any]

class EmbeddingManager:
    """Manages pre-computed embeddings for knowledge base"""
    
    def __init__(self, knowledge_base_path: str, embeddings_cache_path: str = None):
        self.logger = logging.getLogger(__name__)
        self.knowledge_base_path = knowledge_base_path
        
        # Default cache path
        if embeddings_cache_path is None:
            base_dir = os.path.dirname(knowledge_base_path)
            embeddings_cache_path = os.path.join(base_dir, "filum_embeddings.pkl")
        
        self.embeddings_cache_path = embeddings_cache_path
        self.feature_embeddings: Dict[str, FeatureEmbedding] = {}
        self.embedding_model = None
        
    def _load_embedding_model(self):
        """Load sentence transformer model (lazy loading)"""
        if self.embedding_model is None:
            try:
                # This will be imported when needed
                from sentence_transformers import SentenceTransformer
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                self.logger.info("Embedding model loaded successfully")
            except ImportError:
                self.logger.error("sentence-transformers not installed. Run: pip install sentence-transformers")
                raise
            except Exception as e:
                self.logger.error(f"Failed to load embedding model: {e}")
                raise
        return self.embedding_model
    
    def create_text_embedding(self, text: str) -> np.ndarray:
        """Create embedding for a text string"""
        if not text or not text.strip():
            # Return zero vector for empty text
            return np.zeros(384)  # all-MiniLM-L6-v2 dimension
        
        model = self._load_embedding_model()
        return model.encode(text.strip())
    
    def create_feature_embedding(self, feature: Dict[str, Any]) -> FeatureEmbedding:
        """Create comprehensive embedding for a feature"""
        
        # Extract text from 4 target fields
        description = feature.get('description', '')
        pain_points = ' '.join(feature.get('pain_points_addressed', []))
        keywords = ' '.join(feature.get('keywords', []))
        use_cases = ' '.join(feature.get('use_cases', []))
        
        # Create individual embeddings
        desc_emb = self.create_text_embedding(description)
        pain_emb = self.create_text_embedding(pain_points)
        keywords_emb = self.create_text_embedding(keywords)
        use_cases_emb = self.create_text_embedding(use_cases)
        
        # Create combined embedding with weights
        combined_text = f"{description} {pain_points} {keywords} {use_cases}".strip()
        combined_emb = self.create_text_embedding(combined_text)
        
        # Alternative weighted combination
        # combined_emb = (
        #     desc_emb * 0.4 +
        #     pain_emb * 0.3 +
        #     keywords_emb * 0.2 +
        #     use_cases_emb * 0.1
        # )
        
        return FeatureEmbedding(
            feature_id=feature.get('id', ''),
            description_embedding=desc_emb,
            pain_points_embedding=pain_emb,
            keywords_embedding=keywords_emb,
            use_cases_embedding=use_cases_emb,
            combined_embedding=combined_emb,
            metadata={
                'name': feature.get('name', ''),
                'category': feature.get('category', ''),
                'subcategory': feature.get('subcategory', ''),
                'created_at': feature.get('created_at', ''),
            }
        )
    
    def build_embeddings_from_knowledge_base(self) -> Dict[str, FeatureEmbedding]:
        """Build embeddings for all features in knowledge base"""
        self.logger.info(f"Building embeddings from {self.knowledge_base_path}")
        
        # Load knowledge base
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                features = data.get('filum_features', [])
        except Exception as e:
            self.logger.error(f"Failed to load knowledge base: {e}")
            return {}
        
        embeddings = {}
        
        for i, feature in enumerate(features):
            try:
                feature_id = feature.get('id', f'feature_{i}')
                self.logger.info(f"Processing feature {i+1}/{len(features)}: {feature_id}")
                
                embedding = self.create_feature_embedding(feature)
                embeddings[feature_id] = embedding
                
            except Exception as e:
                self.logger.error(f"Failed to create embedding for feature {feature.get('id', i)}: {e}")
                continue
        
        self.feature_embeddings = embeddings
        self.logger.info(f"Successfully created embeddings for {len(embeddings)} features")
        return embeddings
    
    def save_embeddings(self, embeddings: Dict[str, FeatureEmbedding] = None) -> bool:
        """Save embeddings to cache file"""
        if embeddings is None:
            embeddings = self.feature_embeddings
        
        try:
            # Convert to serializable format
            serializable_data = {}
            for feature_id, embedding in embeddings.items():
                serializable_data[feature_id] = {
                    'feature_id': embedding.feature_id,
                    'description_embedding': embedding.description_embedding.tolist(),
                    'pain_points_embedding': embedding.pain_points_embedding.tolist(),
                    'keywords_embedding': embedding.keywords_embedding.tolist(),
                    'use_cases_embedding': embedding.use_cases_embedding.tolist(),
                    'combined_embedding': embedding.combined_embedding.tolist(),
                    'metadata': embedding.metadata
                }
            
            # Save with pickle for numpy arrays (more efficient)
            with open(self.embeddings_cache_path, 'wb') as f:
                pickle.dump(embeddings, f)
            
            # Also save as JSON for inspection
            json_path = self.embeddings_cache_path.replace('.pkl', '.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, indent=2)
            
            self.logger.info(f"Embeddings saved to {self.embeddings_cache_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save embeddings: {e}")
            return False
    
    def load_embeddings(self) -> Dict[str, FeatureEmbedding]:
        """Load embeddings from cache file"""
        try:
            if not os.path.exists(self.embeddings_cache_path):
                self.logger.warning(f"Embeddings cache not found: {self.embeddings_cache_path}")
                return {}
            
            with open(self.embeddings_cache_path, 'rb') as f:
                embeddings = pickle.load(f)
            
            self.feature_embeddings = embeddings
            self.logger.info(f"Loaded embeddings for {len(embeddings)} features")
            return embeddings
            
        except Exception as e:
            self.logger.error(f"Failed to load embeddings: {e}")
            return {}
    
    def get_feature_embedding(self, feature_id: str) -> Optional[FeatureEmbedding]:
        """Get embedding for a specific feature"""
        return self.feature_embeddings.get(feature_id)
    
    def update_single_feature_embedding(self, feature: Dict[str, Any]) -> bool:
        """Update embedding for a single feature"""
        try:
            feature_id = feature.get('id')
            if not feature_id:
                self.logger.error("Feature must have an 'id' field")
                return False
            
            embedding = self.create_feature_embedding(feature)
            self.feature_embeddings[feature_id] = embedding
            
            self.logger.info(f"Updated embedding for feature: {feature_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update feature embedding: {e}")
            return False
    
    def get_embedding_stats(self) -> Dict[str, Any]:
        """Get statistics about current embeddings"""
        if not self.feature_embeddings:
            return {"total_features": 0, "cache_exists": os.path.exists(self.embeddings_cache_path)}
        
        # Calculate some basic stats
        embedding_dims = []
        for embedding in self.feature_embeddings.values():
            embedding_dims.append(embedding.combined_embedding.shape[0])
        
        return {
            "total_features": len(self.feature_embeddings),
            "embedding_dimension": embedding_dims[0] if embedding_dims else 0,
            "cache_file": self.embeddings_cache_path,
            "cache_exists": os.path.exists(self.embeddings_cache_path),
            "feature_ids": list(self.feature_embeddings.keys())
        }
