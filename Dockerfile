FROM alpine:latest

# Install curl, unzip, and supervisor/bash
RUN apk add --no-cache curl bash unzip

# Download and install official Xray-core
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "aarch64" ]; then XRAY_ARCH="arm64-v8a"; else XRAY_ARCH="64"; fi && \
    curl -L -o /tmp/xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-${XRAY_ARCH}.zip && \
    unzip /tmp/xray.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/xray && \
    rm /tmp/xray.zip

# Create config directory
RUN mkdir -p /etc/xray

# Copy your Xray configuration file
COPY config.json /etc/xray/config.json

# Expose Render's dynamic port or default 10000
EXPOSE 10000

# Run Xray server
CMD ["xray", "-config", "/etc/xray/config.json"]
