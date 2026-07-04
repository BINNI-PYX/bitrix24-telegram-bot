from sqlalchemy import or_

from app.db.models import DocumentPage, MessageHistory, User


def get_or_create_user(db, telegram_id, username=None, first_name=None):
    user = db.query(User).filter(User.telegram_id == str(telegram_id)).first()

    if user:
        return user

    user = User(
        telegram_id=str(telegram_id),
        username=username,
        first_name=first_name
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def save_message(db, telegram_id, question, answer):
    message = MessageHistory(
        telegram_id=str(telegram_id),
        question=question,
        answer=answer
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return message


def save_document_page(db, url, title, content):
    page = db.query(DocumentPage).filter(DocumentPage.url == url).first()

    if page:
        page.title = title
        page.content = content
    else:
        page = DocumentPage(url=url, title=title, content=content)
        db.add(page)

    db.commit()
    db.refresh(page)

    return page


def search_documents(db, query, limit=3):
    query_lower = query.lower()

    words = [
        word.lower()
        for word in query.split()
        if len(word) > 2
    ]

    if not words:
        return []

    filters = []
    for word in words:
        filters.append(DocumentPage.title.ilike(f"%{word}%"))
        filters.append(DocumentPage.content.ilike(f"%{word}%"))

    pages = db.query(DocumentPage).filter(or_(*filters)).all()

    scored_pages = []

    for page in pages:
        title = (page.title or "").lower()
        content = (page.content or "").lower()

        score = 0

        if query_lower in title:
            score += 100

        if query_lower in content:
            score += 20

        for word in words:
            if word in title:
                score += 10
            if word in content:
                score += 1

        scored_pages.append((score, page))

    scored_pages.sort(key=lambda item: item[0], reverse=True)

    return [page for score, page in scored_pages[:limit]]
