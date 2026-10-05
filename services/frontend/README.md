# frontend

Mirror's web app: patient sign-in, consent, chat with the expression readout, crisis prompt, and the clinician dashboard. Started from our Lovable prototype; models and the api-gateway are not wired in yet (MS2 Part B / MS3).

**Tech:** React 19 + TanStack Start (server-side rendering), built with Vite and packaged by Nitro for a plain Node server. Uses **npm**, not uv (this is the one JavaScript service).

## Run for development (hot reload)

```bash
npm ci
npm run dev
```

## Run in Docker (production build)

```bash
docker build -t mirror-frontend .
docker run --rm -p 3000:3000 mirror-frontend
```

Open http://localhost:3000.

## Notes

- `NITRO_PRESET=node-server` in the Dockerfile switches the build from Lovable's default (Cloudflare) to a plain Node server.
- Multi-stage image: stage 1 installs and builds, stage 2 keeps only `.output` and runs as the non-root `node` user.
- `node_modules/` and `.output/` are never committed; `package-lock.json` is.
- Port: 3000. Health check: `GET /health`.
- No secrets needed yet. The api-gateway URL will come from an environment variable (Part B).