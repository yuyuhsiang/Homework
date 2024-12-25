import { Application } from "https://deno.land/x/oak/mod.ts";

const app = new Application();

app.use((ctx) => {
  console.log('url=', ctx.request.url);
  let pathname = ctx.request.url.pathname;

  if (pathname == "/") {
    ctx.response.body = `
    <html>
    <body>
    <h1>自我介紹</h1>
    <ol>
    <li><a href="/name">姓名</a></li>
    <li><a href="/age">年紀</a></li>
    <li><a href="/gender">性別</a></li>
    </ol>
    </body>
    </html>
    `;
  } else if (pathname == "/name") {
    ctx.response.body = `
    <html>
    <body>
    <h1>姓名</h1>
    <p>張瑜翔</p>
    <button onclick="location.href='/'">返回主頁</button>
    </body>
    </html>
    `;
  } else if (pathname == "/age") {
    ctx.response.body = `
    <html>
    <body>
    <h1>年紀</h1>
    <p>22</p>
    <button onclick="location.href='/'">返回主頁</button>
    </body>
    </html>
    `;
  } else if (pathname == "/gender") {
    ctx.response.body = `
    <html>
    <body>
    <h1>性別</h1>
    <p>male</p>
    <button onclick="location.href='/'">返回主頁</button>
    </body>
    </html>
    `;
  }
});

console.log('start at : http://127.0.0.1:8000');
await app.listen({ port: 8000 });
