# Multi-stage Dockerfile for building Servo
# Stage 1: Build environment
FROM ubuntu:latest AS builder

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    ccache \
    clang \
    cmake \
    curl \
    g++ \
    git \
    gperf \
    libdbus-1-dev \
    libfreetype6-dev \
    libgl1-mesa-dri \
    libgles2-mesa-dev \
    libglib2.0-dev \
    gstreamer1.0-plugins-good \
    libgstreamer-plugins-good1.0-dev \
    gstreamer1.0-plugins-bad \
    libgstreamer-plugins-bad1.0-dev \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-plugins-base \
    libgstreamer-plugins-base1.0-dev \
    gstreamer1.0-libav \
    libgstrtspserver-1.0-dev \
    gstreamer1.0-tools \
    libges-1.0-dev \
    libharfbuzz-dev \
    liblzma-dev \
    libudev-dev \
    libunwind-dev \
    libvulkan1 \
    libx11-dev \
    libxcb-render0-dev \
    libxcb-shape0-dev \
    libxcb-xfixes0-dev \
    libxmu-dev \
    libxmu6 \
    libegl1-mesa-dev \
    llvm-dev \
    m4 \
    xorg-dev \
    libxkbcommon0 \
    libxkbcommon-x11-0 \
    tshark \
    python3 \
    python3-pip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv for Python dependency management
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Install rustup
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain none
ENV PATH="/root/.cargo/bin:${PATH}"

# Set working directory
WORKDIR /servo

# Copy the entire servo source code
COPY . .

# Set the rust toolchain from rust-toolchain.toml
RUN rustup show

# Bootstrap the build environment
RUN ./mach bootstrap

# Build servo
RUN ./mach build --release

# Stage 2: Runtime environment (optional - for smaller final image)
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libfreetype6 \
    libgl1-mesa-dri \
    libgles2-mesa \
    libglib2.0-0 \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-plugins-base \
    gstreamer1.0-libav \
    libharfbuzz0b \
    libvulkan1 \
    libx11-6 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxmu6 \
    libegl1-mesa \
    libxkbcommon0 \
    libxkbcommon-x11-0 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy the built binary from the builder stage
COPY --from=builder /servo/target/release/servo /usr/local/bin/servo

# Set up a non-root user for running servo
RUN useradd -m -s /bin/bash servo
USER servo
WORKDIR /home/servo

# Set the entry point
ENTRYPOINT ["/usr/local/bin/servo"]
