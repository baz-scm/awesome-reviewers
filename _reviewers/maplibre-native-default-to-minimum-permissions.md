---
title: Default to minimum permissions
description: Always default to the least invasive privacy settings and explicitly
  request elevated permissions only when necessary for specific functionality. For
  location-based features, start with reduced accuracy and request precise location
  only when required with a clear purpose explanation.
repository: maplibre/maplibre-native
label: Security
language: Swift
comments_count: 1
repository_stars: 1411
---

Always default to the least invasive privacy settings and explicitly request elevated permissions only when necessary for specific functionality. For location-based features, start with reduced accuracy and request precise location only when required with a clear purpose explanation.

Configure your app's Info.plist with keys like `NSLocationDefaultAccuracyReduced` to indicate your app can function with reduced permissions by default. This follows the security principle of least privilege and respects user privacy.

Example:
```swift
// In your view model
@Published var locationAccuracy: LocationAccuracyState = .unknown

// Only request higher permissions when necessary with clear purpose
func requestPreciseLocation() {
    if locationAccuracy == .reducedAccuracy {
        let purposeKey = "PreciseLocationPurposeKey" // Defined in InfoPlist.strings
        locationManager.requestTemporaryFullAccuracyAuthorization(withPurposeKey: purposeKey)
    }
}
```

When implementing location features, be careful with properties like `showsUserLocation = true` that might trigger permission requests immediately. Instead, design your app to request permissions contextually when users access specific features that require those permissions.