from dynamic_rest.routers import DynamicRouter

from library import views as libraryViews


router = DynamicRouter()
router.register(r'books', libraryViews.BookViewSet)
router.register(r'authors', libraryViews.AuthorViewSet)
router.register(r'categories', libraryViews.CategoryViewSet)