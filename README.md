# cloudstream-insights  
*Cloud-native Batch & Streaming Analytics Platform*

---

## Executive Summary

*cloudstream-insights* is a cloud-native data platform built to process and analyze both *batch* and *real-time event data* on AWS.  

It demonstrates how to construct a *scalable, cost-efficient, and secure analytics architecture* using managed AWS services. The project combines *traditional batch ETL pipelines* with *real-time streaming analytics*, delivering near-real-time insights from event-driven data sources.

The architecture and implementation follow *consulting-grade best practices: Infrastructure as Code (IaC), clear separation of **data zones, cost control, and **security-by-design*.

---

## Architecture Overview

The platform leverages AWS managed services to separate storage, compute, and analytics layers:

| Layer | Components | Purpose |
|-------|------------|---------|
| Storage | Amazon S3 (Raw / Curated / Analytics) | Central data lake and partitioned storage |
| Batch ETL | AWS Glue | Data ingestion, cleansing, schema enforcement, and quality checks |
| Streaming ETL | Amazon Kinesis Data Streams + Apache Flink | Stateful streaming, deduplication, windowed aggregations |
| Analytics | Amazon Athena & Redshift | Ad-hoc queries and high-performance BI |
| Infrastructure | Terraform | IaC for reproducibility and versioning |
| Monitoring | CloudWatch | ETL monitoring, streaming delays, and alerting |
| Security | IAM & KMS | Least privilege access, encryption at rest and in transit |

---

## Data Flow Explained

### Batch Processing Flow

1. Upload batch data (CSV / JSON / Parquet) to *S3 Raw Zone*  
2. *AWS Glue Jobs* perform:
   - Data cleansing & type enforcement  
   - Schema validation  
   - Data quality checks  
3. Write processed datasets to *S3 Curated Zone*  
4. Query curated data:
   - *Amazon Athena* for ad-hoc analytics  
   - *Amazon Redshift* for structured BI and dashboards  

#### Current Implementation (Python Batch ETL)

- Implemented in etl/glue_jobs/batch_etl.py  
- Features:
  - Robust reading of *JSON Lines* and standard JSON  
  - Automatic *column normalization* and timestamping  
  - Basic *data quality checks* with warnings for missing data  
  - Writes *partitioned Parquet* files to curated S3 zone  

Example:

```python
df = pd.read_json(s3_object)
df.columns = [col.lower().replace(" ", "_") for col in df.columns]
df["processed_at"] = datetime.utcnow()

Streaming Processing Flow
	1.	Event data ingested into Amazon Kinesis Data Streams
	2.	Apache Flink processes streams:
	•	Stateful aggregations & deduplication
	•	Window-based analytics
	•	Exactly-once semantics for reliability
	3.	Writes results to:
	•	S3 (Realtime Curated Zone)
	•	Amazon Redshift for near-real-time dashboards

⸻

Key Design Decisions & Trade-offs
	•	Apache Flink vs AWS Lambda: Flink for stateful streaming & exactly-once semantics
	•	Athena vs Redshift: Athena for ad-hoc, Redshift for BI
	•	Serverless vs Always-On: Serverless preferred for cost-efficiency; Redshift selectively

⸻

Security & Compliance
	•	IAM roles with least privilege
	•	KMS encryption at rest and TLS in transit
	•	Centralized CloudWatch audit logging
	•	Environment separation (dev / prod) via Terraform

⸻

Monitoring & Operations
	•	CloudWatch dashboards for Glue, Kinesis, Flink
	•	Alarms for:
	•	Failed ETL jobs
	•	Streaming delays
	•	Cost thresholds

⸻

Cost Optimization Strategy
	•	S3 lifecycle policies for infrequent access / archival
	•	Athena query optimization (partitions & projection)
	•	Dynamic Kinesis shard scaling
	•	Redshift pause/resume in non-production environments
	•	Monitoring-driven cost alerts

⸻

Project Structure Overview

cloudstream-insights/
├─ infrastructure/  # Terraform for AWS resources
├─ etl/             # Batch ETL & data quality jobs
│  └─ glue_jobs/
│     └─ batch_etl.py
├─ streaming/       # Flink streaming jobs
├─ analytics/       # Athena queries & Redshift models
├─ monitoring/      # Dashboards & alerting
├─ security/        # IAM & encryption docs
├─ costs/           # Cost optimization notes
├─ src/             # Helper scripts (e.g., upload_to_s3.py)
└─ data/            # Sample event files