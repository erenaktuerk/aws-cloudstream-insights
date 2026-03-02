# cloudstream-insights  
*Cloud-native Batch & Streaming Analytics Platform*

## Executive Summary

cloudstream-insights is a cloud-native data platform designed to process and analyze both batch and real-time event data on AWS.

The project demonstrates how to build a scalable, cost-efficient and secure analytics architecture using managed AWS services.  
It combines traditional batch ETL pipelines with real-time streaming analytics to deliver near-real-time insights from event-driven data sources.

The architecture and implementation follow best practices commonly used in IT consulting and data engineering projects, including Infrastructure as Code, clear separation of data zones, cost control mechanisms, and security-by-design.

---

## Architecture Overview

The platform is built on AWS and consists of the following core components:

- *Amazon S3* as the central data lake (Raw, Curated, Analytics zones)
- *AWS Glue* for batch ETL processing and data quality checks
- *Amazon Kinesis Data Streams* for ingesting streaming event data
- *Apache Flink (Kinesis Data Analytics)* for stateful real-time stream processing
- *Amazon Athena* for ad-hoc, cost-efficient analytics
- *Amazon Redshift* for performant BI and dashboard workloads
- *Terraform* for Infrastructure as Code (IaC)
- *Amazon CloudWatch* for monitoring and alerting
- *IAM & KMS* for security and encryption

The platform cleanly separates storage, compute, and analytics layers to enable independent scaling and cost optimization.

---

## Data Flow Explained

### Batch Processing Flow

1. Batch data (CSV / JSON / Parquet) is ingested into *S3 Raw Zone*
2. *AWS Glue Jobs* perform:
   - Data cleansing
   - Schema enforcement
   - Data quality checks
3. Processed data is written to *S3 Curated Zone*
4. Curated data is queried via:
   - *Amazon Athena* for ad-hoc analysis
   - *Amazon Redshift* for structured analytics and reporting

### Streaming Processing Flow

1. Event data is ingested into *Amazon Kinesis Data Streams*
2. *Apache Flink* consumes events and performs:
   - Stateful aggregations
   - Deduplication
   - Window-based analytics
3. Processed streaming data is written to:
   - *S3 (Realtime Curated Zone)*
   - *Amazon Redshift* for near-real-time dashboards

---

## Key Design Decisions & Trade-offs

### Apache Flink vs AWS Lambda
- *Chosen:* Apache Flink  
- *Reason:* Stateful processing, windowed aggregations, exactly-once semantics  
- *Trade-off:* Higher conceptual complexity, but far more suitable for real streaming analytics

### Athena vs Redshift
- *Athena:* Cost-efficient, serverless, ideal for exploratory analytics  
- *Redshift:* Higher performance for BI dashboards and recurring queries  
- *Decision:* Use both depending on workload characteristics

### Serverless vs Always-On Infrastructure
- Preference for serverless services (Glue, Athena, managed Flink)
- Redshift used selectively for performance-critical workloads
- Enables better cost control and operational simplicity

---

## Security & Compliance

Security is implemented following least-privilege and defense-in-depth principles:

- IAM roles with minimal required permissions
- Encryption at rest using AWS KMS
- Encryption in transit using TLS
- Centralized audit logging via CloudWatch and AWS logs
- Environment separation (dev / prod) using Terraform

---

## Monitoring & Operations

The platform includes operational visibility through:

- CloudWatch dashboards for:
  - Glue job execution metrics
  - Kinesis throughput and lag
  - Flink job health and latency
- CloudWatch alarms for:
  - Failed ETL jobs
  - Streaming delays
  - Cost threshold breaches

---

## Cost Optimization Strategy

Cost control is a core design principle:

- S3 lifecycle policies for automatic data tiering
- Athena query optimization and usage limits
- Dynamic scaling of Kinesis shards
- Redshift pause / resume strategy for non-production environments
- Monitoring-based cost alerts

---

## Project Structure Overview

The repository is structured to reflect real-world data engineering projects:

- infrastructure/ – Terraform code for all AWS resources
- etl/ – Glue batch ETL and data quality jobs
- streaming/ – Apache Flink streaming jobs
- analytics/ – Athena queries and Redshift models
- monitoring/ – Dashboards and alerting configuration
- security/ – IAM and encryption documentation
- costs/ – Cost estimation and optimization strategies

---

## Industry Adaptability

The platform is intentionally designed to be industry-agnostic.  
Only the business narrative changes, not the architecture or code.

Examples:
- Finance: Transaction and risk events
- Retail: Orders and clickstream data
- Telco: Network and usage events
- Industry / IoT: Sensor and machine events
- Public Sector: Administrative event data

---

## Key Takeaway

This project demonstrates a consulting-grade cloud data platform that unifies batch and streaming analytics, applies Infrastructure as Code, and balances performance, cost, and operational excellence.

It is intended as a portfolio project showcasing a cloud data engineering mindset rather than a production-ready system. In