# utu_agent_exp_analysis

Frontend pages for utu-agent `exp_analysis`

## Installation
1. Set env of log sql server
```bash
cd frontend/exp_analysis
cp .env.example .env  # config necessary keys...
source .env
```

2. Install next
```bash
npm install next
```

3. Install npm packages
```bash
npm install --legacy-peer-deps
```

The reason for using the `--legacy-peer-deps` option is that the latest version of the `react-json-view` installation package is `1.21.3`. When installed with `react` version `19.0.0`, a warning will be generated. The actual test can be installed and used normally.

## Start using
1. Build your project
```bash
npm run build
```

2. Start your server
```bash
npm run start
```

Once you start your project, the server will be accessible via a browser using your server's IP address and the default port `3000`. If you want to change the default port, you can modify the port in the `start` command in the `script` section of `package.json`.
```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start -p 3000",
    "lint": "next lint",
    "db:migrate": "tsx src/lib/db/migrate.ts",
    "test:db": "tsx scripts/test-db-connection.ts"
  }
}
```

3. Test database connection
```bash
npm run test:db
```
You can call the above command to test whether your database service can be accessed normally. Assuming that the database service has been configured, you can get the first data query in the database by the following command.
