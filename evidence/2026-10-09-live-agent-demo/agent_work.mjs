import { neon } from '@neondatabase/serverless';
import fs from 'node:fs';
const exp = JSON.parse(fs.readFileSync('expected.json'));
const sql = neon(fs.readFileSync('secret/database_url', 'utf8').trim());
await sql.query(`CREATE TABLE humanless_demo_orders (id int primary key, run_tag text not null,
  customer text not null, kind text not null, amount_aud numeric(12,2) not null)`);
for (const r of exp.rows) await sql.query('INSERT INTO humanless_demo_orders VALUES ($1,$2,$3,$4,$5)', r);
const res = await sql.query(exp.expected_query);
const ver = (await sql.query('select version() as v'))[0].v.split(',')[0];
console.log(JSON.stringify({ agent_claim: 'created table humanless_demo_orders, inserted 5 rows, ran summary query',
  summary_query_result: res.map(r => [r.kind, Number(r.count), Number(r.sum)]), server: ver }));
