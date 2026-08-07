plugins {
    id("dev.kikugie.stonecutter")
}

stonecutter active "1.19.2-forge"

stonecutter parameters {
    val loader = current.project.substringAfterLast('-')
    constants {
        match(loader, "forge", "neoforge")
    }
}
