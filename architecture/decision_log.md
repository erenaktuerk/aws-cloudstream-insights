# Architecture Decision Log – cloudstream-insights

This document captures the key architectural decisions made during the design of the cloudstream-insights platform, including rationale and trade-offs.

---

## 1. Data Lake on Amazon S3

*Decision:*  
Amazon S3 is used as the central data lake with separated zones (raw, curated, analytics).

*Rationale:*
- Decouples storage from compute
- Virtually unlimited scalability
- Cost-efficient compared to traditional data warehouses
- Native integration with Glue, Athena, Redshift

*Trade-offs:*
- Requires explicit schema management
- Query performance depends on file format and partitioning

---

## 2. Batch ETL with AWS Glue

*Decision:*  
AWS Glue is used for batch ETL processing and data quality checks.

*Rationale:*
- Fully managed, serverless ETL service
- Tight integration with AWS Data Catalog
- Scales automatically with data volume
- Reduces operational overhead

*Alternatives considered:*
- Custom Spark on EC2 (higher operational cost)
- Lambda-based ETL (not suitable for larger batch workloads)

---

## 3. Streaming Ingestion with Amazon Kinesis

*Decision:*  
Amazon Kinesis Data Streams is used for streaming event ingestion.

*Rationale:*
- Managed, reliable streaming service
- Fine-grained control over throughput via shards
- Native integration with Flink and CloudWatch

*Trade-offs:*
- Requires shard-based capacity planning
- Slightly higher cost than purely serverless alternatives

---

## 4. Stateful Stream Processing with Apache Flink

*Decision:*  
Apache Flink (via Kinesis Data Analytics) is used for real-time processing.

*Rationale:*
- Supports stateful stream processing
- Exactly-once semantics
- Window-based aggregations and deduplication
- Better suited for complex streaming analytics than Lambda

*Why not AWS Lambda:*
- Lambda is stateless
- Complex state handling increases complexity and cost

---

## 5. Analytics Layer: Athena + Redshift

*Decision:*  
Use both Athena and Redshift depending on workload type.

*Rationale:*
- Athena for ad-hoc, cost-efficient queries
- Redshift for performance-critical BI and dashboards
- Enables cost/performance optimization per use case

---

## 6. Infrastructure as Code with Terraform

*Decision:*  
All infrastructure is provisioned using Terraform.

*Rationale:*
- Reproducible environments
- Clear separation between infrastructure and application logic
- Industry-standard in consulting and cloud projects

---

## 7. Security by Design

*Decision:*  
IAM roles are separated by service (Glue, Flink).

*Rationale:*
- Enforces least-privilege principle
- Limits blast radius in case of misconfiguration
- Improves auditability and compliance readiness

---

## 8. Cost Control as First-Class Concern

*Decision:*  
Cost optimization strategies are built into the design.

*Examples:*
- Serverless-first approach
- S3 lifecycle policies
- Redshift pause/resume
- Monitoring-based cost alerts

---

## Summary

The architecture balances scalability, cost efficiency, security, and operational simplicity.  
All decisions are made with real-world cloud consulting constraints in mind.