import graphene
from graphene_django import DjangoObjectType

from wagtailkit.products.models import (
    Product, Inventory, Asset, Service, Bundle,
    ProductCategory, ProductTag
)

from wagtailkit.products.schemas.types import (
    ProductType, InventoryType, AssetType, ServiceType,
    BundleType, ProductCategoryType, ProductTagType
)


class ProductsQuery:
    all_products = graphene.List(ProductType)
    all_inventories = graphene.List(InventoryType)
    all_assets = graphene.List(AssetType)
    all_service = graphene.List(ServiceType)
    all_bundles = graphene.List(BundleType)
    all_product_categories = graphene.List(ProductCategoryType)
    all_product_tags = graphene.List(ProductTagType)

    def resolve_all_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_all_inventories(self, info, **kwargs):
        return Inventory.objects.all()

    def resolve_all_assets(self, info, **kwargs):
        return Asset.objects.all()

    def resolve_all_services(self, info, **kwargs):
        return Service.objects.all()

    def resolve_all_bundles(self, info, **kwargs):
        return Bundle.objects.all()

    def resolve_all_product_categories(self, info, **kwargs):
        return ProductCategory.objects.all()

    def resolve_all_product_tags(self, info, **kwargs):
        return ProductTag.objects.all()
