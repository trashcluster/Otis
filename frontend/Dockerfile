# Multi-stage frontend builder
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig*.json ./
COPY vite.config.ts ./
COPY tailwind.config.js ./
COPY postcss.config.js ./

# Install dependencies
RUN npm ci

# Copy source
COPY src ./src
COPY index.html ./

# Build
RUN npm run build


# Final frontend stage
FROM node:20-alpine

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 otis && adduser -D -u 1001 -G otis otis

# Install lightweight server
RUN npm install -g serve

# Copy built app from builder
COPY --from=builder --chown=otis:otis /app/dist ./dist

# Switch to non-root user
USER otis

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:3000/ || exit 1

CMD ["serve", "-s", "dist", "-l", "3000"]
