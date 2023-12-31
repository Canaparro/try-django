import random


def find_available_slug(instance, slug: str) -> str:
    qs = instance.__class__.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        return find_available_slug(instance, f"{slug}-{random.randint(300_000, 500_000)}")
    else:
        return slug
