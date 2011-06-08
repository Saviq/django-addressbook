from imagekit.specs import ImageSpec
from imagekit import processors
    
class ResizeAdminThumbnail(processors.Resize):
    width = 50
    height = 50
    crop = False
    
class EnhanceSmall(processors.Adjustment):
    contrast = 1.2
    sharpness = 1.1
    
class DjangoAdminThumbnail(ImageSpec):
    access_as = 'admin_thumbnail'
    processors = [ResizeAdminThumbnail, EnhanceSmall]
