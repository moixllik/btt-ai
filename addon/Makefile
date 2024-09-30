VER=$(shell cat ./version.txt)

build: update
	zip btt_ai-$(VER).zip ./__init__.py ./blender_manifest.toml

update:
	sed -i 's/version = "0.0.0"/version = "$(VER)"/g' ./blender_manifest.toml

