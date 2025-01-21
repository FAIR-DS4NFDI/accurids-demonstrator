FROM eclipse-temurin:17-jdk-jammy AS builder

CMD ["gradle"]

ENV GRADLE_HOME=/opt/gradle

RUN set -o errexit -o nounset \
	&& echo "Adding gradle user and group" \
	&& groupadd --system --gid 1000 gradle \
	&& useradd --system --gid gradle --uid 1000 --shell /bin/bash --create-home gradle \
	&& mkdir /home/gradle/.gradle \
	&& chown --recursive gradle:gradle /home/gradle \
	&& chmod --recursive o+rwx /home/gradle \
	\
	&& echo "Symlinking root Gradle cache to gradle Gradle cache" \
	&& ln --symbolic /home/gradle/.gradle /root/.gradle

VOLUME /home/gradle/.gradle

WORKDIR /home/gradle

RUN set -o errexit -o nounset \
	&& apt-get update \
	&& apt-get install --yes --no-install-recommends \
		unzip \
		wget \
		\
		bzr \
		git \
		git-lfs \
		mercurial \
		openssh-client \
		subversion \
	&& rm --recursive --force /var/lib/apt/lists/* \
	\
	&& echo "Testing VCSes" \
	&& which bzr \
	&& which git \
	&& which git-lfs \
	&& which hg \
	&& which svn

ENV GRADLE_VERSION=8.12
ARG GRADLE_DOWNLOAD_SHA256=7a00d51fb93147819aab76024feece20b6b84e420694101f276be952e08bef03
RUN set -o errexit -o nounset \
	&& echo "Downloading Gradle" \
	&& wget --no-verbose --output-document=gradle.zip "https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip" \
	\
	&& echo "Checking Gradle download hash" \
	&& echo "${GRADLE_DOWNLOAD_SHA256} *gradle.zip" | sha256sum --check - \
	\
	&& echo "Installing Gradle" \
	&& unzip gradle.zip \
	&& rm gradle.zip \
	&& mv "gradle-${GRADLE_VERSION}" "${GRADLE_HOME}/" \
	&& ln --symbolic "${GRADLE_HOME}/bin/gradle" /usr/bin/gradle

USER gradle

RUN set -o errexit -o nounset \
	&& echo "Testing Gradle installation" \
	&& gradle --version

USER root

WORKDIR /home

RUN set -o errexit -o nounset \
	&& echo "Cloning EDC Connector repo" \
	&& git clone https://github.com/eclipse-edc/Connector.git \
	&& cd Connector \
	&& git checkout tags/v0.10.1 

ADD launcher/accurids /home/Connector/launchers/accurids
COPY launcher/settings.gradle.kts /home/Connector/settings.gradle.kts

RUN set -o errexit -o nounset \
	&& echo "Building the Accurids launcher" \
	&& echo $PWD \
	&& ls -lah \
	&& cd Connector \
	&& echo $PWD \
	&& ls -lah \
	&& echo "launchers folder:" \
	&& ls -lah launchers \
	&& echo "launchers/accurids folder:" \
	&& ls -lah launchers/accurids \
	&& gradle clean launchers:accurids:build

FROM python:latest
RUN set -o errexit -o nounset \
	&& echo "Installing Java" \
	&& curl -LO https://download.java.net/java/GA/jdk21/fd2272bbf8e04c3dbaee13770090416c/35/GPL/openjdk-21_linux-x64_bin.tar.gz \
	&& tar -xvzf openjdk-21_linux-x64_bin.tar.gz \
	&& echo $PWD \
	&& ls -lah \
	&& export PATH=/jdk-21/bin:$PATH \
	&& export JAVA_HOME=/jdk-21/bin \
	&& java --version

ENV PATH="$PATH:/jdk-21/bin"
ENV JAVA_HOME="/jdk-21/bin"

WORKDIR /home
COPY --from=builder /home/Connector/launchers/accurids/build/libs/accurids-connector.jar .
COPY edc_demo.py ./
COPY run.sh ./
COPY json ./json
COPY launcher/accurids/resources/certs ./certs
COPY launcher/accurids/resources/config ./config
RUN pip install --no-cache-dir requests colorlog jsonpath_ng rich \
	&& echo $PWD \
	&& ls -lah \
	&& echo "json folder" \
	&& ls -lah json \
	&& echo "certs folder" \
	&& ls -lah certs \
	&& echo "config folder" \
	&& ls -lah config \
	&& chmod +x run.sh

RUN set -o errexit -o nounset \
	&& echo "Executing..."

CMD	[ "/home/run.sh" ]
