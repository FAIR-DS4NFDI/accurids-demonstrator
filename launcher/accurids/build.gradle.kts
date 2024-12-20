plugins {
    `java-library`
    id("application")
    alias(libs.plugins.shadow)
}

dependencies {
    implementation(project(":extensions:common:api:control-api-configuration"))
    implementation(project(":extensions:control-plane:api:control-plane-api-client"))
    implementation(project(":extensions:control-plane:api:control-plane-api"))
    implementation(project(":core:control-plane:control-plane-core"))
    implementation(project(":core:common:token-core"))
    implementation(project(":data-protocols:dsp"))
    implementation(project(":extensions:common:http"))
    implementation(project(":extensions:common:configuration:configuration-filesystem"))
    implementation(project(":extensions:common:iam:iam-mock"))
    implementation(project(":extensions:control-plane:api:management-api"))
    implementation(project(":extensions:control-plane:transfer:transfer-data-plane-signaling"))
    implementation(project(":extensions:control-plane:transfer:transfer-pull-http-receiver"))
    implementation(project(":extensions:common:validator:validator-data-address-http-data"))
    implementation(project(":extensions:control-plane:api:management-api:edr-cache-api"))
    implementation(project(":core:common:edr-store-core"))
    implementation(project(":extensions:control-plane:edr:edr-store-receiver"))
    implementation(project(":extensions:data-plane-selector:data-plane-selector-api"))
    implementation(project(":core:data-plane-selector:data-plane-selector-core"))
    implementation(project(":extensions:data-plane:data-plane-self-registration"))
    implementation(project(":extensions:data-plane:data-plane-signaling:data-plane-signaling-api"))
    implementation(project(":extensions:data-plane:data-plane-public-api-v2"))
    implementation(project(":core:data-plane:data-plane-core"))
    implementation(project(":extensions:data-plane:data-plane-http"))
    implementation(project(":extensions:data-plane:data-plane-iam"))
}

application {
    mainClass.set("org.eclipse.edc.boot.system.runtime.BaseRuntime")
}

tasks.withType<com.github.jengelman.gradle.plugins.shadow.tasks.ShadowJar> {
    exclude("**/pom.properties", "**/pom.xm", "jndi.properties", "jetty-dir.css", "META-INF/maven/**")
    mergeServiceFiles()
    archiveFileName.set("accurids-connector.jar")
}

edcBuild {
    publish.set(false)
}
