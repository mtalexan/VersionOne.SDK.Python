from v1pysdk import V1Meta

v1 = V1Meta()

my_story = v1.Story('1005')

print(my_story.Name)
# 'New Story 2'
my_story.Owners
# [<v1pysdk.v1meta.Member object at 0x02AD9710>]
my_story.Scope
# <v1pysdk.v1meta.Scope object at 0x02AB2550>


for my_story in v1.Story.where(Name='New Story 2'):
  print(my_story.Name)


