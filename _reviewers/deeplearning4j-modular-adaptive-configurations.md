---
title: Modular adaptive configurations
description: Structure configuration scripts with modularity and adaptability in mind.
  Extract repeated parameters into variables, separate parameter construction from
  command execution, and use dynamic detection for environment-specific values instead
  of hardcoding them. This approach improves readability, maintainability, and resilience
  to changes in the environment.
repository: deeplearning4j/deeplearning4j
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 14036
---

Structure configuration scripts with modularity and adaptability in mind. Extract repeated parameters into variables, separate parameter construction from command execution, and use dynamic detection for environment-specific values instead of hardcoding them. This approach improves readability, maintainability, and resilience to changes in the environment.

Example:
```bash
# Instead of repeating parameters in each condition:
if [ "${HELPER}" != '' ] && [ "${EXTENSION}" != '' ]; then
    command="mvn -Possrh -Djavacpp.platform.extension=-${HELPER}-${EXTENSION} ... -DskipTests"
elif [ "${HELPER}" != '' ]; then
    command="mvn -Possrh -Djavacpp.platform.extension=-${HELPER} ... -DskipTests"
else
    command="mvn -Possrh -Djavacpp.platform.extension=${EXTENSION} ... -DskipTests"
fi

# Prefer modular construction:
common_params="-Possrh -Dlibnd4j.buildThreads=${buildThreads} -Djavacpp.platform=linux-x86_64 -Dlibnd4j.chip=cuda --also-make -Pcuda clean --batch-mode package deploy -DskipTests"

if [ "${HELPER}" != '' ] && [ "${EXTENSION}" != '' ]; then
    mvn_ext="-Djavacpp.platform.extension=-${HELPER}-${EXTENSION} -Dlibnd4j.helper=${HELPER} -Dlibnd4j.extension=${EXTENSION}"
elif [ "${HELPER}" != '' ]; then
    mvn_ext="-Djavacpp.platform.extension=-${HELPER} -Dlibnd4j.helper=${HELPER}"
else
    mvn_ext="-Djavacpp.platform.extension=${EXTENSION}"
fi

command="mvn ${common_params} ${mvn_ext}"

# Use dynamic version detection instead of hardcoding:
# Instead of: sudo cp /usr/lib/gcc/x86_64-linux-gnu/5.5.0/libgomp.so /usr/lib
gcc_version=$(gcc --version | head -n 1 | grep -o '[^ ]*$')
sudo cp /usr/lib/gcc/x86_64-linux-gnu/${gcc_version}/libgomp.so /usr/lib
```