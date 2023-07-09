from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from comment import Theme
import requests

app = FastAPI()
themes = ["vitaminD3", "omega3"]
templates = Jinja2Templates(directory="../templates")
info_themes = {
    "vitaminD3" : [Theme("мне нравится это", "negative")],
    "omega3" : [Theme("оо это то что мне нужно было")]
}
for i in range(1, 101):
    theme_key = f"theme{i}"
    theme_comment = f"Comment for theme {i}"
    info_themes[theme_key] = [Theme(theme_comment)]
    themes.append(theme_key)
for i in range(1, 50):
    info_themes["vitaminD3"].append(Theme(f"мне нравится этоt коммент номер {i}"))


@app.get("/")
def index(request: Request, page : int = 1):
    l = 10
    next_page = page + 1
    k = 0
    if(len(themes) % l != 0):
        k = 1
    if(next_page > (len(themes) // l + k)):
        next_page = 1
    return templates.TemplateResponse("main.html",
            {"request": request,
             "themes" : themes[l * (page - 1):l*page],
             "next_page" : next_page
            }   
    )

@app.get("/{theme}")
def some_page_with_theme(request : Request, theme : str = "", page : int = 1):
    l = 3
    next_page = page + 1
    k = 0
    if(len(info_themes[theme]) % l != 0):
        k = 1
    if(next_page > (len(info_themes[theme]) // l + k)):
        next_page = 1
    information = info_themes[theme][l * (page - 1):l*page]
    return templates.TemplateResponse("theme.html",
            {
                "request" : request,
                "information" : information,
                "theme" : theme,
                "next_page" : next_page
            }
    )
    
@app.post("/download")
def post_info_to_theme(request : Request,theme : str = Form(), comment : str = Form(), type : str = Form()):
    if theme in info_themes:
        body = Theme(comment, type)
        info_themes[theme].append(body)
    else:
        body = Theme(comment, type)
        info_themes[theme] = [body]
        themes.append(theme)
    
    return RedirectResponse(f"/{theme}", status_code=303)