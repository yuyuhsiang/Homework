import { Application } from "https://deno.land/x/oak/mod.ts";

const app = new Application();

app.use((ctx) => {
  console.log('url=', ctx.request.url)
  let pathname = ctx.request.url.pathname
  if(pathname == "/"){
    ctx.response.body = `
    <html>
    <body>
    <h1>自我介紹</h1>
    <ol>
    <li><a href = "/name">姓名</a></li>
    <li><a href = "/age">年紀</a></li>
    <li><a href = "/gender">性別</a></li>
    </ol>
    </body>
    </html>
    `
  }
  if(pathname == "/name"){
    ctx.response.body = "張瑜翔"
  }
  if(pathname == "/age"){
    ctx.response.body = "22"
  }
  if(pathname == "/gender"){
    ctx.response.body = "femail"
  }
});

console.log('start at : http://127.0.0.1:8000')
await app.listen({ port: 8000 })