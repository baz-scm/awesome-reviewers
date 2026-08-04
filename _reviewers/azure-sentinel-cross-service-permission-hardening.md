---
title: Cross-service Permission Hardening
description: When granting permissions across AWS services (S3→SQS, EventBridge→Lambda,
  etc.), use the correct permission model and apply least-privilege constraints to
  prevent confused-deputy and silent authorization failures.
repository: Azure/Azure-Sentinel
label: Security
language: Yaml
comments_count: 4
repository_stars: 6042
---

When granting permissions across AWS services (S3→SQS, EventBridge→Lambda, etc.), use the correct permission model and apply least-privilege constraints to prevent confused-deputy and silent authorization failures.

Apply this checklist:
1) Use resource-based permissions for the target
- For service-to-service invocation (e.g., EventBridge invoking Lambda), grant access with the target’s resource-based policy (e.g., `AWS::Lambda::Permission`). Don’t rely on IAM roles placed on the event target—those may be ignored.

2) Never use overly broad principals in cross-service queue/object policies
- Avoid `Principal: "*"` when a service principal can be specified (e.g., `Service: s3.amazonaws.com`).

3) Constrain cross-service grants with SourceArn + SourceAccount
- Add both `aws:SourceArn` (bucket/route) and `aws:SourceAccount` (deploying account) conditions so only events from the intended resource/account can trigger the permission.

4) Scope IAM wildcards to concrete resources
- Replace `Resource: "*"` with ARNs that match only the required log groups/buckets/paths; similarly pin logging permissions to the specific function log group.

Example: S3 notifications to SQS (confused-deputy hardening)
```yaml
SentinelSQSQueuePolicy:
  Type: AWS::SQS::QueuePolicy
  Properties:
    Queues:
      - !Ref SentinelSQSQueue
    PolicyDocument:
      Version: '2012-10-17'
      Statement:
        - Sid: AllowS3ToSendMessages
          Effect: Allow
          Principal:
            Service: s3.amazonaws.com
          Action: SQS:SendMessage
          Resource: !GetAtt SentinelSQSQueue.Arn
          Condition:
            ArnLike:
              aws:SourceArn: !Sub arn:${AWS::Partition}:s3:::${LogBucketName}
            StringEquals:
              aws:SourceAccount: !Ref AWS::AccountId
```

Example: EventBridge invoking Lambda (correct permission mechanism)
```yaml
EventInvokePermission:
  Type: AWS::Lambda::Permission
  Properties:
    Action: lambda:InvokeFunction
    FunctionName: !GetAtt ExporterLambda.Arn
    Principal: events.amazonaws.com
    SourceArn: !Ref EventBridgeRuleArn
```

Result: fewer authorization surprises, reduced privilege, and protection against cross-service abuse patterns.