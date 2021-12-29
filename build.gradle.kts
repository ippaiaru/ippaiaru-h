import kr.entree.spigradle.kotlin.*

plugins {
    kotlin("jvm") version "1.3.72"
    id("com.github.johnrengelman.shadow") version "5.2.0"
    id("kr.entree.spigradle") version "2.2.3"
    kotlin("plugin.serialization") version "1.3.72"
}

group = "AlphaGot"
version = "0.0.2a"

repositories {
    mavenCentral()
    maven(url = "https://papermc.io/repo/repository/maven-public/") //paper
    maven(url = "https://repo.dmulloy2.net/nexus/repository/public/") //protocollib
    maven(url = "https://jitpack.io/") //tap, psychic
    maven(url = "https://maven.enginehub.org/repo/") //worldedit
    jcenter()
}

dependencies {
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.0.1")
    compileOnly(kotlin("stdlib-jdk8")) //kotlin
    compileOnly("junit:junit:4.12") //junit
    compileOnly(paper("1.16.3"))
    compileOnly("com.comphenix.protocol:ProtocolLib:4.6.0-SNAPSHOT") //protocollib
    compileOnly("com.github.noonmaru:tap:2.8.8") //tap
    compileOnly("com.sk89q.worldedit:worldedit-bukkit:7.1.0") //worldedit
}

tasks {
    compileJava {
        options.encoding = "UTF-8"
    }
    javadoc {
        options.encoding = "UTF-8"
    }
    compileKotlin {
        kotlinOptions.jvmTarget = "1.8"
    }
    compileTestKotlin {
        kotlinOptions.jvmTarget = "1.8"
    }
    processResources {
        filesMatching("**/*.yml") {
            expand(project.properties)
        }
    }
    shadowJar {
        archiveClassifier.set("dist")
    }
    create<Copy>("distJar") {
        from(shadowJar)
        into("F:\\th-like-danmaku\\dist")
    }
}

if (!hasProperty("debug")) {
    tasks {
        shadowJar {
            relocate("com.alphagot.danmaku", "com.alphagot.danmaku.shaded")
        }
    }
}