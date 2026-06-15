# Optimizing Delivery ETAs with Graph-Based Network Intelligence

## Overview

This project develops a graph-based intelligence system for a large-scale logistics network inspired by Delhivery's hub-and-spoke operations. Traditional ETA estimation systems rely heavily on shortest-path routing engines such as OSRM, which often underestimate actual delivery times due to operational bottlenecks, facility dwell times, traffic congestion, and route-specific delays.

The objective of this project is to model the logistics network as a directed graph, leverage graph analytics and node embeddings, improve ETA prediction accuracy, identify bottleneck hubs and delayed corridors, and provide actionable operational recommendations.

---

## Live Dashboard

**Streamlit Application:**

https://traffic-analysis-app-ezse6aeztkgddqsgeasgan.streamlit.app

The dashboard provides:

* Network-wide bottleneck analysis
* Corridor delay monitoring
* Route type distribution analysis
* ETA model performance comparison
* Operational intelligence insights

---

## Problem Statement

Key business challenges addressed:

* ETA predictions frequently underestimate actual delivery times.
* SLA breaches impact customer satisfaction and operational efficiency.
* Critical bottleneck hubs are difficult to identify systematically.
* Route selection decisions often ignore network-level risk.
* Delayed corridors create downstream planning and capacity issues.

This project uses graph-based network intelligence to address these challenges.

---

## Dataset

The dataset consists of logistics trip segments containing:

* Source and destination facilities
* Actual travel times
* OSRM travel times
* Route types (FTL and Carting)
* Segment-level distances
* Trip timestamps
* Corridor information

**Note:** Dataset is not included in this repository due to competition restrictions.

---

## Methodology

### 1. Data Preparation

* Data cleaning and preprocessing
* Missing value analysis
* Feature engineering
* Delay ratio calculation
* Time-based feature creation

### 2. Graph Construction

A directed logistics network was created where:

* Nodes represent facilities/hubs
* Edges represent shipment corridors
* Edge weights capture corridor-level delay characteristics

### 3. Network Analysis

Computed graph metrics:

* Betweenness Centrality
* Degree Centrality
* In-Degree / Out-Degree
* Closeness Centrality
* Eigenvector Centrality
* PageRank
* Clustering Coefficient

These metrics were used to identify structurally important hubs and network bottlenecks.

### 4. Bottleneck Detection

Critical hubs and delayed corridors were identified using:

* Centrality measures
* Delay ratios
* Corridor-level risk indicators
* Structural risk scoring

### 5. ETA Prediction

#### Baseline Model

Traditional machine learning model using trip-level features.

#### Graph-Enhanced Model

Node2Vec graph embeddings were generated and incorporated into the prediction pipeline to capture network structure and facility relationships.

### 6. FTL vs Carting Framework

A route-type recommendation framework was developed to evaluate trade-offs between:

* Transit time
* Operational efficiency
* Corridor characteristics
* Network position

---

## Key Results

### ETA Prediction Improvement

The graph-enhanced model outperformed the baseline model by leveraging network structure and facility relationships.

Key improvements include:

* Lower prediction error
* Better ETA reliability
* Improved operational visibility

### Network Intelligence

The analysis successfully identified:

* High-risk bottleneck hubs
* Chronic delay corridors
* Critical network dependencies
* Route-specific operational risks

---

## Technology Stack

* Python
* Pandas
* NumPy
* NetworkX
* Node2Vec
* Scikit-Learn
* XGBoost
* Matplotlib
* Seaborn
* Plotly
* Streamlit


---

## Future Enhancements

* GraphSAGE-based node embeddings
* Real-time ETA prediction pipeline
* Dynamic traffic integration
* Route optimization engine
* Advanced network resilience analysis

---

## Author

Shagun

Data Science | Machine Learning | Graph Analytics | Business Intelligence
