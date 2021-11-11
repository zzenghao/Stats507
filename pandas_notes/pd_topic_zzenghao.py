# + [markdown] slideshow={"slide_type": "slide"}
# # Zane Zhang  zzenghao@umich.edu

# + [markdown] slideshow={"slide_type": "slide"}
# # Filling missing values

# + [markdown] slideshow={"slide_type": "fragment"}
# > Creat a dataframe with nan value

# + slideshow={"slide_type": "fragment"}
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(5, 3),
    index=["a", "c", "d", "e", "f"],
    columns=["one", "two", "three"],
)

df=df.reindex(["a", "b", "c", "d", "e", "f"])
df

# + [markdown] slideshow={"slide_type": "slide"}
# ## filna() method
# * fillna() can “fill in” NA values with non-NA data in a couple of ways
#     * Replace NA with a scalar value
#     
#     
# **fill the nan value with -1**

# + slideshow={"slide_type": "fragment"}
df.fillna(-1)

# + [markdown] slideshow={"slide_type": "subslide"}
# **fill nan with string**

# + slideshow={"slide_type": "fragment"}
df.fillna("missing")

# + [markdown] slideshow={"slide_type": "slide"}
# ## filna() method
# * fillna() can “fill in” NA values with non-NA data in a couple of ways
#     * Fill gaps forward(method="Pad") or backward(method="bfill")

# + slideshow={"slide_type": "fragment"}
print("fill the data based on the forward data")
print(df.fillna(method="pad"))
print("fill the data based on the backward data")
print(df.fillna(method="bfill"))
