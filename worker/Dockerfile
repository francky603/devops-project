# Build stage
FROM openjdk:11-jdk-slim AS build
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y maven
RUN mvn package

# Run stage
FROM openjdk:11-jre-slim
WORKDIR /app
COPY --from=build /app/target/worker-1.0-SNAPSHOT.jar /app/worker.jar
CMD ["java", "-jar", "worker.jar"]
