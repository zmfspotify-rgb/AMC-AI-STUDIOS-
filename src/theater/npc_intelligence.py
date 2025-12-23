"""NPC Audience Intelligence System - Reviews, ratings, and influence."""

import logging
import uuid
import random
from typing import List, Dict
from datetime import datetime

from src.core.config import Config
from src.models.schema import Project, NPCState, NPCReview


class NPCAudienceIntelligence:
    """Manages NPC reviews, ratings, and influence on studio decisions."""
    
    def __init__(self, config: Config):
        """Initialize NPC audience intelligence."""
        self.config = config
        self.logger = logging.getLogger("AMCStudios.NPCIntelligence")
        
        # Review storage
        self.reviews: Dict[str, List[NPCReview]] = {}
        
        # Box office tracking
        self.box_office: Dict[str, Dict] = {}
        
        self.logger.info("NPC Audience Intelligence initialized")
    
    def generate_npc_review(
        self,
        npc: NPCState,
        project: Project,
        emotional_reactions: List[str]
    ) -> NPCReview:
        """
        Generate an NPC review after watching a movie.
        
        Args:
            npc: The NPC who watched
            project: The project watched
            emotional_reactions: List of emotional reactions during viewing
            
        Returns:
            Generated review
        """
        # Base rating on genre preferences and emotional reactions
        rating = self._calculate_rating(project, emotional_reactions)
        sentiment = self._determine_sentiment(rating)
        review_text = self._generate_review_text(npc, project, rating, emotional_reactions)
        
        review = NPCReview(
            review_id=str(uuid.uuid4()),
            npc_id=npc.id,
            npc_name=npc.name,
            project_id=project.id,
            rating=rating,
            sentiment=sentiment,
            review_text=review_text,
            emotional_reaction=emotional_reactions
        )
        
        # Store review
        if project.id not in self.reviews:
            self.reviews[project.id] = []
        self.reviews[project.id].append(review)
        
        # Update project's aggregate rating
        self._update_project_rating(project)
        
        self.logger.info(f"NPC {npc.name} reviewed {project.title}: {rating}/10")
        return review
    
    def _calculate_rating(self, project: Project, reactions: List[str]) -> float:
        """Calculate rating based on project and reactions."""
        base_rating = 7.0
        
        # Positive reactions boost rating
        positive_reactions = ["laugh", "clap", "cheer", "gasp_positive"]
        negative_reactions = ["gasp_negative", "confused", "bored"]
        
        positive_count = sum(1 for r in reactions if r in positive_reactions)
        negative_count = sum(1 for r in reactions if r in negative_reactions)
        
        rating = base_rating + (positive_count * 0.5) - (negative_count * 0.7)
        
        # Add some randomness
        rating += random.uniform(-0.8, 0.8)
        
        # Clamp to 0-10
        return max(0.0, min(10.0, rating))
    
    def _determine_sentiment(self, rating: float) -> str:
        """Determine sentiment from rating."""
        if rating >= 7.5:
            return "positive"
        elif rating <= 4.5:
            return "negative"
        else:
            return "mixed"
    
    def _generate_review_text(
        self,
        npc: NPCState,
        project: Project,
        rating: float,
        reactions: List[str]
    ) -> str:
        """Generate review text."""
        
        if rating >= 8.5:
            templates = [
                f"Absolutely loved {project.title}! A must-watch!",
                f"{project.title} exceeded all my expectations. Brilliant!",
                f"One of the best {project.project_type.value}s I've seen this year!",
                f"Couldn't take my eyes off the screen. {project.title} is a masterpiece!"
            ]
        elif rating >= 7.0:
            templates = [
                f"{project.title} was really enjoyable. Definitely worth watching!",
                f"Had a great time watching {project.title}. Solid entertainment!",
                f"Really enjoyed {project.title}. Would recommend!",
                f"Good movie! {project.title} delivered on its promise."
            ]
        elif rating >= 5.0:
            templates = [
                f"{project.title} was okay. Had its moments.",
                f"Mixed feelings about {project.title}. Some parts were good.",
                f"{project.title} was decent, but nothing special.",
                f"Not bad, not great. {project.title} was average."
            ]
        else:
            templates = [
                f"Disappointed by {project.title}. Expected more.",
                f"{project.title} didn't work for me unfortunately.",
                f"Had high hopes for {project.title} but it fell flat.",
                f"Not my cup of tea. {project.title} missed the mark."
            ]
        
        return random.choice(templates)
    
    def _update_project_rating(self, project: Project):
        """Update project's aggregate rating."""
        if project.id not in self.reviews:
            return
        
        reviews = self.reviews[project.id]
        if not reviews:
            return
        
        total_rating = sum(r.rating for r in reviews)
        project.average_rating = total_rating / len(reviews)
        
        # Store reviews in project
        project.npc_reviews = [
            {
                "npc_name": r.npc_name,
                "rating": r.rating,
                "sentiment": r.sentiment,
                "text": r.review_text
            }
            for r in reviews[-10:]  # Last 10 reviews
        ]
    
    def track_box_office(self, project: Project, npc_count: int):
        """
        Track box office performance based on NPC attendance.
        
        Args:
            project: Project being watched
            npc_count: Number of NPCs watching
        """
        ticket_price = 12.50
        revenue = npc_count * ticket_price
        
        if project.id not in self.box_office:
            self.box_office[project.id] = {
                "total_viewers": 0,
                "total_revenue": 0.0,
                "showings": 0
            }
        
        self.box_office[project.id]["total_viewers"] += npc_count
        self.box_office[project.id]["total_revenue"] += revenue
        self.box_office[project.id]["showings"] += 1
        
        # Update project
        project.box_office_total = self.box_office[project.id]["total_revenue"]
        
        self.logger.info(
            f"Box office update for {project.title}: "
            f"${self.box_office[project.id]['total_revenue']:.2f}"
        )
    
    def should_greenlight_sequel(self, project: Project) -> Dict:
        """
        Determine if a sequel should be greenlit based on performance.
        
        Args:
            project: Project to evaluate
            
        Returns:
            Decision dict with recommendation and reasons
        """
        decision = {
            "recommended": False,
            "confidence": 0.0,
            "reasons": []
        }
        
        # Check rating
        if project.average_rating >= 7.5:
            decision["recommended"] = True
            decision["confidence"] += 0.4
            decision["reasons"].append(f"Strong audience rating: {project.average_rating:.1f}/10")
        elif project.average_rating < 5.0:
            decision["reasons"].append(f"Low audience rating: {project.average_rating:.1f}/10")
            return decision
        
        # Check box office
        if project.id in self.box_office:
            box_office_data = self.box_office[project.id]
            
            if box_office_data["total_revenue"] >= 10000:
                decision["recommended"] = True
                decision["confidence"] += 0.3
                decision["reasons"].append(
                    f"Strong box office: ${box_office_data['total_revenue']:.2f}"
                )
            
            if box_office_data["total_viewers"] >= 500:
                decision["confidence"] += 0.2
                decision["reasons"].append(
                    f"High viewership: {box_office_data['total_viewers']} viewers"
                )
        
        # Check reviews sentiment
        if project.id in self.reviews:
            reviews = self.reviews[project.id]
            positive_reviews = sum(1 for r in reviews if r.sentiment == "positive")
            
            if positive_reviews / len(reviews) >= 0.7:
                decision["recommended"] = True
                decision["confidence"] += 0.1
                decision["reasons"].append(
                    f"Positive sentiment: {positive_reviews}/{len(reviews)} reviews"
                )
        
        # Final decision
        if decision["recommended"] and decision["confidence"] >= 0.6:
            decision["recommendation"] = "GREENLIGHT"
        elif decision["confidence"] >= 0.4:
            decision["recommendation"] = "CONSIDER"
        else:
            decision["recommendation"] = "PASS"
        
        return decision
    
    def get_trending_projects(self) -> List[Dict]:
        """
        Get trending projects based on recent activity.
        
        Returns:
            List of trending project data
        """
        trending = []
        
        for project_id, box_office_data in self.box_office.items():
            if box_office_data["showings"] >= 3:  # Active project
                trending.append({
                    "project_id": project_id,
                    "viewers": box_office_data["total_viewers"],
                    "revenue": box_office_data["total_revenue"],
                    "trend_score": box_office_data["total_viewers"] * 
                                  (box_office_data["total_revenue"] / 1000)
                })
        
        # Sort by trend score
        trending.sort(key=lambda x: x["trend_score"], reverse=True)
        
        return trending[:5]  # Top 5
    
    def get_project_analytics(self, project: Project) -> Dict:
        """
        Get comprehensive analytics for a project.
        
        Args:
            project: Project to analyze
            
        Returns:
            Analytics dict
        """
        analytics = {
            "project_id": project.id,
            "title": project.title,
            "average_rating": project.average_rating,
            "total_reviews": len(self.reviews.get(project.id, [])),
            "box_office": self.box_office.get(project.id, {}),
            "sentiment_breakdown": self._get_sentiment_breakdown(project.id),
            "sequel_recommendation": self.should_greenlight_sequel(project)
        }
        
        return analytics
    
    def _get_sentiment_breakdown(self, project_id: str) -> Dict:
        """Get sentiment distribution for reviews."""
        if project_id not in self.reviews:
            return {"positive": 0, "negative": 0, "mixed": 0}
        
        reviews = self.reviews[project_id]
        breakdown = {"positive": 0, "negative": 0, "mixed": 0}
        
        for review in reviews:
            breakdown[review.sentiment] += 1
        
        return breakdown
