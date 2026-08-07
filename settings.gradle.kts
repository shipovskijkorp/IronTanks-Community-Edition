pluginManagement {
    repositories {
        mavenCentral()
        gradlePluginPortal()
        maven("https://maven.minecraftforge.net") { name = "MinecraftForge" }
        maven("https://maven.neoforged.net/releases") { name = "NeoForged" }
        maven("https://maven.kikugie.dev/releases") { name = "KikuGie Releases" }
    }
}

plugins {
    id("org.gradle.toolchains.foojay-resolver-convention") version "0.8.0"
    id("dev.kikugie.stonecutter") version "0.7.11"
}

logger.lifecycle("IronTanks configuration: Stonecutter 0.7.11 + Gradle 8.8; four targets declared inline")

stonecutter {
    create(rootProject) {
        version("1.19.2-forge", "1.19.2").buildscript("build.forge.gradle")
        version("1.20.1-forge", "1.20.1").buildscript("build.forge.gradle")
        version("1.21.1-forge", "1.21.1").buildscript("build.forge.gradle")
        version("1.21.1-neoforge", "1.21.1").buildscript("build.neoforge.gradle")
        vcsVersion = "1.19.2-forge"
    }
}

rootProject.name = "IronTanks"
