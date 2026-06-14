# ---------- Builder stage ----------
FROM node:20-alpine AS builder
WORKDIR /app

# Install all dependencies (including devDependencies like typescript)
COPY package*.json ./
RUN npm ci

# Copy source files
COPY . .

# Generate Prisma client and build TypeScript
RUN npx prisma generate
RUN npm run build

# Prune devDependencies to keep the runtime image light
RUN npm prune --omit=dev

# ---------- Runtime stage ----------
FROM node:20-alpine
WORKDIR /app

# Install curl for healthcheck and openssl compatibility for Prisma
RUN apk add --no-cache curl libssl1.1 --repository=http://dl-cdn.alpinelinux.org/alpine/v3.16/main

# Copy only the compiled output and production dependencies
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/prisma ./prisma
COPY --from=builder /app/package*.json ./

EXPOSE 8081

# Default command runs the compiled server
CMD ["node", "dist/server.js"]
