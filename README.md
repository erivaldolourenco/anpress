# Anpress CMS

Mini CMS em Django 5.2 inspirado no conceito do WordPress: simples, moderno e escalável.

## Funcionalidades

- Dashboard próprio com login/logout
- CRUD de posts, páginas e usuários
- Busca, filtros por status e paginação no dashboard
- Área pública com Home, Blog, detalhe de post e páginas institucionais por slug
- Sistema de tema ativo via configuração do site (`SiteSetting`)
- Tema padrão `anpress-default`
- SEO básico (`meta_title` e `meta_description`)
- `sitemap.xml` e `robots.txt`

## Estrutura

- `core`: configurações do site, home, contexto global e sitemap
- `blog`: posts públicos
- `pages`: páginas institucionais
- `dashboard`: painel administrativo próprio
- `themes/anpress-default`: templates do tema público
- `static/themes/anpress-default`: estilos do tema

## Como rodar

1. Ative o ambiente virtual:

```bash
source venv/bin/activate
```

2. Aplique migrações:

```bash
python manage.py migrate
```

3. Crie superusuário:

```bash
python manage.py createsuperuser
```

4. Rode o servidor:

```bash
python manage.py runserver
```

## URLs principais

- Site público: `http://127.0.0.1:8000/`
- Blog: `http://127.0.0.1:8000/blog/`
- Dashboard: `http://127.0.0.1:8000/dashboard/`
- Admin Django: `http://127.0.0.1:8000/admin/`
- Sitemap: `http://127.0.0.1:8000/sitemap.xml`
- Robots: `http://127.0.0.1:8000/robots.txt`

## Tema ativo

O tema é definido em `SiteSetting.active_theme`.

Tema inicial disponível:

- `anpress-default`
