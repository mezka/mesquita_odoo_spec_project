from django.db import models

# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField()

class ProductAttribute(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductAttributeValue(models.Model):
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductTemplate(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    attributes = models.ManyToManyField(ProductAttribute, through='ProductTemplateAttributeLine', related_name='templates')
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ProductTemplateAttributeLine(models.Model):
    template = models.ForeignKey(ProductTemplate, on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    values = models.ManyToManyField(ProductAttributeValue)

    class Meta:
        unique_together = ('template', 'attribute')

    def __str__(self):
        return f"{self.template.name} - {self.attribute.name}"


class ProductVariant(models.Model):
    template = models.ForeignKey(ProductTemplate, on_delete=models.CASCADE, related_name='variants')
    attributes = models.ManyToManyField(ProductAttributeValue)

    def __str__(self):
        attributes = ', '.join(str(attr.value) for attr in self.attributes.all())
        return f"{self.template.name} ({attributes})"