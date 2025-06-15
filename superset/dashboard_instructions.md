# Superset Dashboard Setup

1. Created a view `heymax-analytics.heymax_datamart.view_user_growth_summary` to store all the metrics used in the charts.
2. Connect Superset to BigQuery
3. Add `heymax-analytics.heymax_datamart.view_user_growth_summary` as dataset
4. Create charts:
   - DAU/WAU/MAU: Count distinct user_id over time
   - New vs Retained: Compare first_seen vs activity
   - Triangle Retention: Cohort matrix
5. Pin charts to a dashboard
