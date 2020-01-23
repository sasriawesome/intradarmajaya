from graphene_django import DjangoObjectType

from wagtailkit.products.models import (
    Product, Inventory, Asset, Service, Bundle,
    ProductCategory, ProductTag
)


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class InventoryType(DjangoObjectType):
    class Meta:
        model = Inventory


class AssetType(DjangoObjectType):
    class Meta:
        model = Asset


class ServiceType(DjangoObjectType):
    class Meta:
        model = Service


class BundleType(DjangoObjectType):
    class Meta:
        model = Bundle


class ProductCategoryType(DjangoObjectType):
    class Meta:
        model = ProductCategory


class ProductTagType(DjangoObjectType):
    class Meta:
        model = ProductTag
