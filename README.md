# BounceBack — Customer Retention & Churn Risk Prediction System

## Overview
BounceBack is an automated customer engagement system designed to predict churn risk and send personalized retention messages based on user interaction data. It analyzes user activity to identify at-risk users and triggers real-time SMS notifications to improve retention.

## Features
- Tracks user activity: time spent, pages viewed, last visit date.
- Calculates Interaction Score with weighted formula (α=0.4, β=0.4, γ=0.2).
- Flags users with Interaction Score < 0.6 as uninterested.
- Sends personalized SMS notifications via Twilio.
- Stores interaction data using Supabase with CSV uploads.
- Trains a neural network model on sample data using Python (Google Colab).

## Technologies Used
- Python (ML model training and backend)
- Supabase (PostgreSQL, CSV data storage)
- Twilio API (SMS notifications)
- JavaScript, HTML/CSS (if applicable frontend)
- Neural Networks (Google Colab)

## Interaction Score Formula

Where α=0.4, β=0.4, γ=0.2

-Interaction Score = α × (Time Spent / max Time Spent) + β × (Pages Viewed / max Pages Viewed) + γ × (1 / (1 + Days Since Last Visit))

## Getting Started

### Prerequisites
- Python 3.x
- Supabase project and credentials
- Twilio account and API keys

### Installation
1. Clone the repo:
2. Install dependencies:
3. Configure environment variables for Supabase and Twilio.

### Usage
- Upload user interaction CSV files to Supabase.
- Train the neural network on sample data in Google Colab.
- Run the backend to compute scores and send notifications.
- Monitor user engagement results.

