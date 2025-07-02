---
title: Preserve API compatibility
description: "When evolving APIs, maintain backward compatibility to prevent breaking\
  \ changes for existing consumers. \n\nKey approaches:\n\n1. **Retain removed members\
  \ with obsolete attributes**: When removing or replacing public methods, mark the\
  \ original as obsolete but maintain its functionality."
repository: Azure/azure-sdk-for-net
label: API
language: C#
comments_count: 5
repository_stars: 5809
---

When evolving APIs, maintain backward compatibility to prevent breaking changes for existing consumers. 

Key approaches:

1. **Retain removed members with obsolete attributes**: When removing or replacing public methods, mark the original as obsolete but maintain its functionality.

```csharp
// Old method
[EditorBrowsable(EditorBrowsableState.Never)]
[Obsolete("Use UpdateAsync(WaitUntil, ConnectorPatch) instead")]
public virtual Response<ConnectorResource> Update(ConnectorPatch patch, 
    CancellationToken cancellationToken = default)
{
    // Call the new implementation
    return UpdateAsync(WaitUntil.Completed, patch, cancellationToken).EnsureCompleted();
}

// New method
public virtual ArmOperation<ConnectorResource> Update(WaitUntil waitUntil, 
    ConnectorPatch patch, CancellationToken cancellationToken = default)
```

2. **Handle constructor parameter changes**: When a required parameter becomes optional, keep a constructor overload that accepts the previously required parameter:

```csharp
// Old constructor required publisherId
public MarketplaceDetails(string planId, string offerId, string publisherId) 
    : this(planId, offerId)
{
    PublisherId = publisherId;
}

// New constructor makes publisherId optional
public MarketplaceDetails(string planId, string offerId) { }
```

3. **Add code-gen attributes for serialization**: When properties are removed from models, use code generation attributes to maintain serialization compatibility:

```csharp
[CodeGenSerialization(nameof(BlockResponseCode), "blockResponseCode")]
public partial class DnsSecurityRuleAction
{
    [EditorBrowsable(EditorBrowsableState.Never)]
    public BlockResponseCode? BlockResponseCode { get; set; }
}
```

These approaches ensure that existing code continues to work while allowing APIs to evolve with improved designs.


[
  {
    "discussion_id": "2171177846",
    "pr_number": 50739,
    "pr_file": "sdk/qumulo/Azure.ResourceManager.Qumulo/api/Azure.ResourceManager.Qumulo.net8.0.cs",
    "created_at": "2025-06-27T08:18:03+00:00",
    "commented_code": "}\n    public partial class MarketplaceDetails : System.ClientModel.Primitives.IJsonModel<Azure.ResourceManager.Qumulo.Models.MarketplaceDetails>, System.ClientModel.Primitives.IPersistableModel<Azure.ResourceManager.Qumulo.Models.MarketplaceDetails>\n    {\n        public MarketplaceDetails(string planId, string offerId, string publisherId) { }\n        public MarketplaceDetails(string planId, string offerId) { }",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2171177846",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50739,
        "pr_file": "sdk/qumulo/Azure.ResourceManager.Qumulo/api/Azure.ResourceManager.Qumulo.net8.0.cs",
        "discussion_id": "2171177846",
        "commented_code": "@@ -124,25 +116,39 @@ protected virtual void JsonModelWriteCore(System.Text.Json.Utf8JsonWriter writer\n     }\n     public partial class MarketplaceDetails : System.ClientModel.Primitives.IJsonModel<Azure.ResourceManager.Qumulo.Models.MarketplaceDetails>, System.ClientModel.Primitives.IPersistableModel<Azure.ResourceManager.Qumulo.Models.MarketplaceDetails>\n     {\n-        public MarketplaceDetails(string planId, string offerId, string publisherId) { }\n+        public MarketplaceDetails(string planId, string offerId) { }",
        "comment_created_at": "2025-06-27T08:18:03+00:00",
        "comment_author": "ArcturusZhang",
        "comment_body": "So `publisherId` is no longer required in the new api-version.\r\nThis is not breaking from the spec's perspective, but we must do something on the .net code to make it non-breaking.\r\n\r\nPlease add a partial class with the same namespace and same name as this class, and put it in `sdk/qumulo/Azure.ResourceManager.Qumulo/src/Customized/Models`, and we need to add the missing members back, like this:\r\n```\r\nnamespace Azure.ResourceManager.Qumulo\r\n{\r\n\t// we will need the xml doc back, you should be able to find it in git history.\r\n\tpublic partial class MarketplaceDetails(string planId, string offerId, string publisherId) : this(planId, offerId)\r\n\t{\r\n\t\tPublisherId = publisherId;\r\n\t}\r\n}\r\n```",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2125382124",
    "pr_number": 50381,
    "pr_file": "sdk/sqlmanagement/Azure.ResourceManager.Sql/src/Custom/ElasticPoolResource.cs",
    "created_at": "2025-06-04T02:48:30+00:00",
    "commented_code": "_sqlDatabaseDatabasesRestClient = new DatabasesRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint, sqlDatabaseDatabasesApiVersion);\n            _elasticPoolOperationsClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n            _elasticPoolOperationsRestClient = new ElasticPoolRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n            _elasticPoolActivitiesClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n            _elasticPoolActivitiesRestClient = new ElasticPoolActivitiesRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n            _elasticPoolDatabaseActivitiesRestClient = new ElasticPoolDatabaseActivitiesRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n            _elasticPoolDatabaseActivitiesClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n            _metricDefinitionsClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n            _metricDefinitionsRestClient = new MetricDefinitionsRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n            _metricsClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n            _metricsRestClient = new MetricsRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n#if DEBUG\n            ValidateResourceId(Id);\n#endif\n        }\n\n        /// <summary>\n        /// Returns elastic pool activities.\n        /// <list type=\"bullet\">\n        /// <item>\n        /// <term>Request Path</term>\n        /// <description>/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Sql/servers/{serverName}/elasticPools/{elasticPoolName}/elasticPoolActivity</description>\n        /// </item>\n        /// <item>\n        /// <term>Operation Id</term>\n        /// <description>ElasticPoolActivities_ListByElasticPool</description>\n        /// </item>\n        /// <item>\n        /// <term>Default Api Version</term>\n        /// <description>2014-04-01</description>\n        /// </item>\n        /// </list>\n        /// </summary>\n        /// <param name=\"cancellationToken\"> The cancellation token to use. </param>\n        /// <returns> An async collection of <see cref=\"ElasticPoolActivity\"/> that may take multiple service requests to iterate over. </returns>\n        public virtual AsyncPageable<ElasticPoolActivity> GetElasticPoolActivitiesAsync(CancellationToken cancellationToken = default)",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2125382124",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50381,
        "pr_file": "sdk/sqlmanagement/Azure.ResourceManager.Sql/src/Custom/ElasticPoolResource.cs",
        "discussion_id": "2125382124",
        "commented_code": "@@ -39,225 +30,9 @@ internal ElasticPoolResource(ArmClient client, ResourceIdentifier id) : base(cli\n             _sqlDatabaseDatabasesRestClient = new DatabasesRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint, sqlDatabaseDatabasesApiVersion);\n             _elasticPoolOperationsClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n             _elasticPoolOperationsRestClient = new ElasticPoolRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n-            _elasticPoolActivitiesClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n-            _elasticPoolActivitiesRestClient = new ElasticPoolActivitiesRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n-            _elasticPoolDatabaseActivitiesRestClient = new ElasticPoolDatabaseActivitiesRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n-            _elasticPoolDatabaseActivitiesClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n-            _metricDefinitionsClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n-            _metricDefinitionsRestClient = new MetricDefinitionsRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n-            _metricsClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n-            _metricsRestClient = new MetricsRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n #if DEBUG\n             ValidateResourceId(Id);\n #endif\n         }\n-\n-        /// <summary>\n-        /// Returns elastic pool activities.\n-        /// <list type=\"bullet\">\n-        /// <item>\n-        /// <term>Request Path</term>\n-        /// <description>/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Sql/servers/{serverName}/elasticPools/{elasticPoolName}/elasticPoolActivity</description>\n-        /// </item>\n-        /// <item>\n-        /// <term>Operation Id</term>\n-        /// <description>ElasticPoolActivities_ListByElasticPool</description>\n-        /// </item>\n-        /// <item>\n-        /// <term>Default Api Version</term>\n-        /// <description>2014-04-01</description>\n-        /// </item>\n-        /// </list>\n-        /// </summary>\n-        /// <param name=\"cancellationToken\"> The cancellation token to use. </param>\n-        /// <returns> An async collection of <see cref=\"ElasticPoolActivity\"/> that may take multiple service requests to iterate over. </returns>\n-        public virtual AsyncPageable<ElasticPoolActivity> GetElasticPoolActivitiesAsync(CancellationToken cancellationToken = default)",
        "comment_created_at": "2025-06-04T02:48:30+00:00",
        "comment_author": "ArthurMa1978",
        "comment_body": "Please retain all public members, but mark them as obsolete.",
        "pr_file_module": null
      },
      {
        "comment_id": "2125389119",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50381,
        "pr_file": "sdk/sqlmanagement/Azure.ResourceManager.Sql/src/Custom/ElasticPoolResource.cs",
        "discussion_id": "2125382124",
        "commented_code": "@@ -39,225 +30,9 @@ internal ElasticPoolResource(ArmClient client, ResourceIdentifier id) : base(cli\n             _sqlDatabaseDatabasesRestClient = new DatabasesRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint, sqlDatabaseDatabasesApiVersion);\n             _elasticPoolOperationsClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n             _elasticPoolOperationsRestClient = new ElasticPoolRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n-            _elasticPoolActivitiesClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n-            _elasticPoolActivitiesRestClient = new ElasticPoolActivitiesRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n-            _elasticPoolDatabaseActivitiesRestClient = new ElasticPoolDatabaseActivitiesRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n-            _elasticPoolDatabaseActivitiesClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n-            _metricDefinitionsClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n-            _metricDefinitionsRestClient = new MetricDefinitionsRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n-            _metricsClientDiagnostics = new ClientDiagnostics(\"Azure.ResourceManager.Sql\", ProviderConstants.DefaultProviderNamespace, Diagnostics);\n-            _metricsRestClient = new MetricsRestOperations(Pipeline, Diagnostics.ApplicationId, Endpoint);\n #if DEBUG\n             ValidateResourceId(Id);\n #endif\n         }\n-\n-        /// <summary>\n-        /// Returns elastic pool activities.\n-        /// <list type=\"bullet\">\n-        /// <item>\n-        /// <term>Request Path</term>\n-        /// <description>/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Sql/servers/{serverName}/elasticPools/{elasticPoolName}/elasticPoolActivity</description>\n-        /// </item>\n-        /// <item>\n-        /// <term>Operation Id</term>\n-        /// <description>ElasticPoolActivities_ListByElasticPool</description>\n-        /// </item>\n-        /// <item>\n-        /// <term>Default Api Version</term>\n-        /// <description>2014-04-01</description>\n-        /// </item>\n-        /// </list>\n-        /// </summary>\n-        /// <param name=\"cancellationToken\"> The cancellation token to use. </param>\n-        /// <returns> An async collection of <see cref=\"ElasticPoolActivity\"/> that may take multiple service requests to iterate over. </returns>\n-        public virtual AsyncPageable<ElasticPoolActivity> GetElasticPoolActivitiesAsync(CancellationToken cancellationToken = default)",
        "comment_created_at": "2025-06-04T02:51:55+00:00",
        "comment_author": "ArthurMa1978",
        "comment_body": "Run 'eng\\scripts\\Export-API.ps1 sqlmanagement' after mark it as obsolete.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2086177848",
    "pr_number": 49921,
    "pr_file": "sdk/dnsresolver/Azure.ResourceManager.DnsResolver/tests/Tests/DnsSecurityRuleTests.cs",
    "created_at": "2025-05-13T07:59:25+00:00",
    "commented_code": "// ARRANGE\n            var dnsSecurityRuleName = Recording.GenerateAssetName(\"dnsSecurityRule-\");\n            await CreateDnsResolverCollection();",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2086177848",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 49921,
        "pr_file": "sdk/dnsresolver/Azure.ResourceManager.DnsResolver/tests/Tests/DnsSecurityRuleTests.cs",
        "discussion_id": "2086177848",
        "commented_code": "@@ -58,7 +59,7 @@ public async Task CreateDnsSecurityRule()\n             // ARRANGE\n             var dnsSecurityRuleName = Recording.GenerateAssetName(\"dnsSecurityRule-\");\n             await CreateDnsResolverCollection();",
        "comment_created_at": "2025-05-13T07:59:25+00:00",
        "comment_author": "Copilot",
        "comment_body": "The removal of the BlockResponseCode property from the DnsSecurityRuleAction requires that both tests and documentation explicitly acknowledge this breaking change. Consider updating any relevant comments or documentation to clarify the new usage.\n```suggestion\n            await CreateDnsResolverCollection();\n            // The BlockResponseCode property has been removed from DnsSecurityRuleAction.\n            // The ActionType property should now be used to specify the desired action (e.g., Block).\n```",
        "pr_file_module": null
      },
      {
        "comment_id": "2087159144",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 49921,
        "pr_file": "sdk/dnsresolver/Azure.ResourceManager.DnsResolver/tests/Tests/DnsSecurityRuleTests.cs",
        "discussion_id": "2086177848",
        "commented_code": "@@ -58,7 +59,7 @@ public async Task CreateDnsSecurityRule()\n             // ARRANGE\n             var dnsSecurityRuleName = Recording.GenerateAssetName(\"dnsSecurityRule-\");\n             await CreateDnsResolverCollection();",
        "comment_created_at": "2025-05-13T15:53:29+00:00",
        "comment_author": "jamesvoongms",
        "comment_body": "Added breaking change comment, customers can no longer specify the blockresponsecode, tests also reflect this.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2092317865",
    "pr_number": 49921,
    "pr_file": "sdk/dnsresolver/Azure.ResourceManager.DnsResolver/api/Azure.ResourceManager.DnsResolver.net8.0.cs",
    "created_at": "2025-05-16T04:53:31+00:00",
    "commented_code": "{\n        public DnsSecurityRuleAction() { }\n        public Azure.ResourceManager.DnsResolver.Models.DnsSecurityRuleActionType? ActionType { get { throw null; } set { } }\n        public Azure.ResourceManager.DnsResolver.Models.BlockResponseCode? BlockResponseCode { get { throw null; } set { } }",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2092317865",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 49921,
        "pr_file": "sdk/dnsresolver/Azure.ResourceManager.DnsResolver/api/Azure.ResourceManager.DnsResolver.net8.0.cs",
        "discussion_id": "2092317865",
        "commented_code": "@@ -865,7 +882,6 @@ public partial class DnsSecurityRuleAction : System.ClientModel.Primitives.IJson\n     {\n         public DnsSecurityRuleAction() { }\n         public Azure.ResourceManager.DnsResolver.Models.DnsSecurityRuleActionType? ActionType { get { throw null; } set { } }\n-        public Azure.ResourceManager.DnsResolver.Models.BlockResponseCode? BlockResponseCode { get { throw null; } set { } }",
        "comment_created_at": "2025-05-16T04:53:31+00:00",
        "comment_author": "ArcturusZhang",
        "comment_body": "this is a breaking change.\r\nIn order to find a way to mitigate it, I need to know what happened to this property. Could you share some information about how this property changed in your spec?\r\nWe removed it in the latest api-version, I know this for sure.\r\nWould the older existing api-versions still support this property? Or this property is a mistake from its first day.\r\nThe answer to these questions could change the way how we mitigate this.",
        "pr_file_module": null
      },
      {
        "comment_id": "2092328678",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 49921,
        "pr_file": "sdk/dnsresolver/Azure.ResourceManager.DnsResolver/api/Azure.ResourceManager.DnsResolver.net8.0.cs",
        "discussion_id": "2092317865",
        "commented_code": "@@ -865,7 +882,6 @@ public partial class DnsSecurityRuleAction : System.ClientModel.Primitives.IJson\n     {\n         public DnsSecurityRuleAction() { }\n         public Azure.ResourceManager.DnsResolver.Models.DnsSecurityRuleActionType? ActionType { get { throw null; } set { } }\n-        public Azure.ResourceManager.DnsResolver.Models.BlockResponseCode? BlockResponseCode { get { throw null; } set { } }",
        "comment_created_at": "2025-05-16T05:07:28+00:00",
        "comment_author": "jamesvoongms",
        "comment_body": "Yes the older existing api-versions will support this property.\r\n\r\nFor more details, this property essentially is ignored on the control plane side, whatever the customer provides in this field is ignored and defaulted to a different value, and so the intention is to remove it.\r\n\r\nEven on the old API versions, the value is being ignored on the old api versions but we are allowing customers to provide the parameter on old API versions.\r\n\r\nIdeally we would like to remove it on all API versions as it being ignored in all API versions in the control plane standpoint.",
        "pr_file_module": null
      },
      {
        "comment_id": "2092459604",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 49921,
        "pr_file": "sdk/dnsresolver/Azure.ResourceManager.DnsResolver/api/Azure.ResourceManager.DnsResolver.net8.0.cs",
        "discussion_id": "2092317865",
        "commented_code": "@@ -865,7 +882,6 @@ public partial class DnsSecurityRuleAction : System.ClientModel.Primitives.IJson\n     {\n         public DnsSecurityRuleAction() { }\n         public Azure.ResourceManager.DnsResolver.Models.DnsSecurityRuleActionType? ActionType { get { throw null; } set { } }\n-        public Azure.ResourceManager.DnsResolver.Models.BlockResponseCode? BlockResponseCode { get { throw null; } set { } }",
        "comment_created_at": "2025-05-16T07:03:46+00:00",
        "comment_author": "ArcturusZhang",
        "comment_body": "If this is the case, we need to introduce this property back to mitigate the breaking change:\r\nPlease create a partial class in `src/Customization` or `src/Custom` directory for this class:\r\n```\r\nnamespace Azure.ResourceManager.DnsResolver.Models\r\n{\r\n\t[CodeGenSerialization(nameof(BlockResponseCode), \"blockResponseCode\")]\r\n\tpublic partial class DnsSecurityRuleAction\r\n\t{\r\n\t\t[EditorBrowsable(EditorBrowsableState.Never)]\r\n\t\tpublic BlockResponseCode? BlockResponseCode { get; set; }\r\n\t}\r\n}\r\n```\r\nThe `EditorBrowsable` attribute hides this property from the intellisence so that new users would not see it, and the `CodeGenSerialization` attribute lets the generator know about how to serialize/deserialize this property into/from the payload to make sure the generated SDK could work with previous API versions.\r\n\r\nDuring this process, the type of this property `BlockResponseCode` may also be deleted in this update, please find the removed file from git history and move it to the `src/Customization` or `src/Custom` directory.\r\nAfter you have introduced the above code, please run the `dotnet build /t:GenerateCode` command to regenerate everything.",
        "pr_file_module": null
      },
      {
        "comment_id": "2099563338",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 49921,
        "pr_file": "sdk/dnsresolver/Azure.ResourceManager.DnsResolver/api/Azure.ResourceManager.DnsResolver.net8.0.cs",
        "discussion_id": "2092317865",
        "commented_code": "@@ -865,7 +882,6 @@ public partial class DnsSecurityRuleAction : System.ClientModel.Primitives.IJson\n     {\n         public DnsSecurityRuleAction() { }\n         public Azure.ResourceManager.DnsResolver.Models.DnsSecurityRuleActionType? ActionType { get { throw null; } set { } }\n-        public Azure.ResourceManager.DnsResolver.Models.BlockResponseCode? BlockResponseCode { get { throw null; } set { } }",
        "comment_created_at": "2025-05-21T07:26:41+00:00",
        "comment_author": "jamesvoongms",
        "comment_body": "I have added the deleted blockresponsecode.cs back into customization and the dnsSecurityRuleACtion but these seems to cause issues in the generator\r\n\r\nPS C:\\Git\\jamesvoong-azure-sdk-for-net\\sdk\\dnsresolver\\Azure.ResourceManager.DnsResolver> dotnet build /t:GenerateCode\r\nRestore complete (1.1s)\r\n  Azure.ResourceManager.DnsResolver failed with 2 error(s) (11.3s)\r\n    EXEC : error   | error : Plugin csharpgen reported failure.\r\n    Q:\\.tools\\.nuget\\packages\\microsoft.azure.autorest.csharp\\3.0.0-beta.20250512.2\\buildMultiTargeting\\Microsoft.Azure.AutoRest.CSharp.targets(59,5): error MSB3073: The command \"npx autorest@ --max-memory-size=8192 --skip-csproj --skip-upgrade-check --version=3.9.7 C:\\Git\\jamesvoong-azure-sdk-for-net\\sdk\\dnsresolver\\Azure.ResourceManager.DnsResolver\\src/autorest.md  --use=Q:\\.tools\\.nuget\\packages\\microsoft.azure.autorest.csharp\\3.0.0-beta.20250512.2\\buildMultiTargeting\\../tools/net9.0/any/ --clear-output-folder=true --shared-source-folders=\"C:\\Git\\jamesvoong-azure-sdk-for-net\\eng\\/../sdk/core/Azure.Core/src/Shared/;Q:\\.tools\\.nuget\\packages\\microsoft.azure.autorest.csharp\\3.0.0-beta.20250512.2\\buildMultiTargeting\\../content/Generator.Shared/\" --output-folder=C:\\Git\\jamesvoong-azure-sdk-for-net\\sdk\\dnsresolver\\Azure.ResourceManager.DnsResolver\\src/Generated --namespace=Azure.ResourceManager.DnsResolver\" exited with code 1.\r\n\r\nBuild failed with 2 error(s) in 12.7s\r\n\r\nWorkload updates are available. Run `dotnet workload list` for more information.",
        "pr_file_module": null
      }
    ]
  },
  {
    "discussion_id": "2104107019",
    "pr_number": 50236,
    "pr_file": "sdk/containerapps/Azure.ResourceManager.AppContainers/api/Azure.ResourceManager.AppContainers.net8.0.cs",
    "created_at": "2025-05-23T08:35:10+00:00",
    "commented_code": "Azure.ResourceManager.AppContainers.ContainerAppCertificateData System.ClientModel.Primitives.IPersistableModel<Azure.ResourceManager.AppContainers.ContainerAppCertificateData>.Create(System.BinaryData data, System.ClientModel.Primitives.ModelReaderWriterOptions options) { throw null; }\n        string System.ClientModel.Primitives.IPersistableModel<Azure.ResourceManager.AppContainers.ContainerAppCertificateData>.GetFormatFromOptions(System.ClientModel.Primitives.ModelReaderWriterOptions options) { throw null; }\n        System.BinaryData System.ClientModel.Primitives.IPersistableModel<Azure.ResourceManager.AppContainers.ContainerAppCertificateData>.Write(System.ClientModel.Primitives.ModelReaderWriterOptions options) { throw null; }\n        public virtual Azure.Response<Azure.ResourceManager.AppContainers.ContainerAppConnectedEnvironmentCertificateResource> Update(Azure.ResourceManager.AppContainers.Models.ContainerAppCertificatePatch patch, System.Threading.CancellationToken cancellationToken = default(System.Threading.CancellationToken)) { throw null; }\n        public virtual System.Threading.Tasks.Task<Azure.Response<Azure.ResourceManager.AppContainers.ContainerAppConnectedEnvironmentCertificateResource>> UpdateAsync(Azure.ResourceManager.AppContainers.Models.ContainerAppCertificatePatch patch, System.Threading.CancellationToken cancellationToken = default(System.Threading.CancellationToken)) { throw null; }\n        public virtual Azure.ResourceManager.ArmOperation<Azure.ResourceManager.AppContainers.ContainerAppConnectedEnvironmentCertificateResource> Update(Azure.WaitUntil waitUntil, Azure.ResourceManager.AppContainers.Models.ContainerAppCertificatePatch patch, System.Threading.CancellationToken cancellationToken = default(System.Threading.CancellationToken)) { throw null; }",
    "repo_full_name": "Azure/azure-sdk-for-net",
    "discussion_comments": [
      {
        "comment_id": "2104107019",
        "repo_full_name": "Azure/azure-sdk-for-net",
        "pr_number": 50236,
        "pr_file": "sdk/containerapps/Azure.ResourceManager.AppContainers/api/Azure.ResourceManager.AppContainers.net8.0.cs",
        "discussion_id": "2104107019",
        "commented_code": "@@ -186,8 +442,8 @@ protected ContainerAppConnectedEnvironmentCertificateResource() { }\n         Azure.ResourceManager.AppContainers.ContainerAppCertificateData System.ClientModel.Primitives.IPersistableModel<Azure.ResourceManager.AppContainers.ContainerAppCertificateData>.Create(System.BinaryData data, System.ClientModel.Primitives.ModelReaderWriterOptions options) { throw null; }\n         string System.ClientModel.Primitives.IPersistableModel<Azure.ResourceManager.AppContainers.ContainerAppCertificateData>.GetFormatFromOptions(System.ClientModel.Primitives.ModelReaderWriterOptions options) { throw null; }\n         System.BinaryData System.ClientModel.Primitives.IPersistableModel<Azure.ResourceManager.AppContainers.ContainerAppCertificateData>.Write(System.ClientModel.Primitives.ModelReaderWriterOptions options) { throw null; }\n-        public virtual Azure.Response<Azure.ResourceManager.AppContainers.ContainerAppConnectedEnvironmentCertificateResource> Update(Azure.ResourceManager.AppContainers.Models.ContainerAppCertificatePatch patch, System.Threading.CancellationToken cancellationToken = default(System.Threading.CancellationToken)) { throw null; }\n-        public virtual System.Threading.Tasks.Task<Azure.Response<Azure.ResourceManager.AppContainers.ContainerAppConnectedEnvironmentCertificateResource>> UpdateAsync(Azure.ResourceManager.AppContainers.Models.ContainerAppCertificatePatch patch, System.Threading.CancellationToken cancellationToken = default(System.Threading.CancellationToken)) { throw null; }\n+        public virtual Azure.ResourceManager.ArmOperation<Azure.ResourceManager.AppContainers.ContainerAppConnectedEnvironmentCertificateResource> Update(Azure.WaitUntil waitUntil, Azure.ResourceManager.AppContainers.Models.ContainerAppCertificatePatch patch, System.Threading.CancellationToken cancellationToken = default(System.Threading.CancellationToken)) { throw null; }",
        "comment_created_at": "2025-05-23T08:35:10+00:00",
        "comment_author": "ArcturusZhang",
        "comment_body": "here is a breaking change.\r\nwe should introduce the removed overload back.\r\nits implementation could just call this new one.",
        "pr_file_module": null
      }
    ]
  }
]
