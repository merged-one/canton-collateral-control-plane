#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
. "$script_dir/toolchain.env"

runtime_dir="$repo_root/.runtime"
downloads_dir="$runtime_dir/downloads"
tools_dir="$runtime_dir/tools"
bin_dir="$runtime_dir/bin"
daml_home_dir="$runtime_dir/daml-home"
venv_dir="$repo_root/.venv"

need_cmd() {
	command -v "$1" >/dev/null 2>&1 || {
		echo "bootstrap: missing required command '$1'" >&2
		exit 1
	}
}

sha256_file() {
	if command -v shasum >/dev/null 2>&1; then
		shasum -a 256 "$1" | awk '{print $1}'
	elif command -v sha256sum >/dev/null 2>&1; then
		sha256sum "$1" | awk '{print $1}'
	else
		echo "bootstrap: need shasum or sha256sum to verify downloads" >&2
		exit 1
	fi
}

download_if_needed() {
	target_path=$1
	url=$2
	expected_sha=$3

	if [ -f "$target_path" ] && [ "$(sha256_file "$target_path")" = "$expected_sha" ]; then
		return
	fi

	rm -f "$target_path"
	curl -fsSL "$url" -o "$target_path"
	actual_sha=$(sha256_file "$target_path")
	[ "$actual_sha" = "$expected_sha" ] || {
		echo "bootstrap: checksum mismatch for $target_path" >&2
		echo "bootstrap: expected $expected_sha" >&2
		echo "bootstrap: actual   $actual_sha" >&2
		exit 1
	}
}

install_archive() {
	archive_path=$1
	extracted_root=$2
	destination=$3

	[ -d "$destination" ] && return

	tmpdir=$(mktemp -d)
	trap 'rm -rf "$tmpdir"' EXIT HUP INT TERM
	tar -xzf "$archive_path" -C "$tmpdir"
	test -d "$tmpdir/$extracted_root" || {
		echo "bootstrap: expected extracted directory $extracted_root" >&2
		exit 1
	}
	rm -rf "$destination"
	mv "$tmpdir/$extracted_root" "$destination"
	rm -rf "$tmpdir"
	trap - EXIT HUP INT TERM
}

write_daml_home() {
	mkdir -p "$daml_home_dir/sdk"
	ln -sfn "$1" "$daml_home_dir/sdk/$DAML_SDK_VERSION"
	cat > "$daml_home_dir/daml-config.yaml" <<EOF
update-check: never
auto-install: false
EOF
}

write_env_file() {
	java_home=$1
	daml_home=$2
	daml_sdk_root=$3

	cat > "$runtime_dir/env.sh" <<EOF
export REPO_ROOT="$repo_root"
export RUNTIME_DIR="$runtime_dir"
export JAVA_HOME="$java_home"
export DAML_HOME="$daml_home"
export DAML_SDK_ROOT="$daml_sdk_root"
export PATH="$bin_dir:\$PATH"
export DAML_BIN="$bin_dir/daml"
export DAML_HELPER_BIN="$bin_dir/daml-helper"
export PYTHON_BIN="$venv_dir/bin/python"
export CHECK_JSONSCHEMA_BIN="$venv_dir/bin/check-jsonschema"
EOF
}

need_cmd curl
need_cmd tar
need_cmd python3
need_cmd make
need_cmd rg

mkdir -p "$downloads_dir" "$tools_dir" "$bin_dir"

platform="$(uname -s)-$(uname -m)"

case "$platform" in
	Darwin-arm64)
		daml_archive=$DAML_SDK_MACOS_ARM64_ARCHIVE
		daml_url=$DAML_SDK_MACOS_ARM64_URL
		daml_sha=$DAML_SDK_MACOS_ARM64_SHA256
		jdk_archive=$JAVA_MACOS_ARM64_ARCHIVE
		jdk_url=$JAVA_MACOS_ARM64_URL
		jdk_sha=$JAVA_MACOS_ARM64_SHA256
		jdk_root="jdk-$JAVA_VERSION"
		java_home_suffix="Contents/Home"
		;;
	Linux-x86_64)
		daml_archive=$DAML_SDK_LINUX_X64_ARCHIVE
		daml_url=$DAML_SDK_LINUX_X64_URL
		daml_sha=$DAML_SDK_LINUX_X64_SHA256
		jdk_archive=$JAVA_LINUX_X64_ARCHIVE
		jdk_url=$JAVA_LINUX_X64_URL
		jdk_sha=$JAVA_LINUX_X64_SHA256
		jdk_root="jdk-$JAVA_VERSION"
		java_home_suffix=""
		;;
	*)
		echo "bootstrap: unsupported platform $platform" >&2
		echo "bootstrap: supported platforms are Darwin-arm64 and Linux-x86_64" >&2
		exit 1
		;;
esac

daml_download="$downloads_dir/$daml_archive"
jdk_download="$downloads_dir/$jdk_archive"
daml_install="$tools_dir/daml-sdk-$DAML_SDK_VERSION"
jdk_install="$tools_dir/jdk-$JAVA_VERSION"

download_if_needed "$daml_download" "$daml_url" "$daml_sha"
download_if_needed "$jdk_download" "$jdk_url" "$jdk_sha"

install_archive "$daml_download" "sdk-$DAML_SDK_VERSION" "$daml_install"
install_archive "$jdk_download" "$jdk_root" "$jdk_install"

if [ -n "$java_home_suffix" ]; then
	java_home="$jdk_install/$java_home_suffix"
else
	java_home="$jdk_install"
fi

ln -sf "$daml_install/daml/daml" "$bin_dir/daml"
ln -sf "$daml_install/daml-helper/daml-helper" "$bin_dir/daml-helper"
ln -sf "$java_home/bin/java" "$bin_dir/java"
ln -sf "$java_home/bin/javac" "$bin_dir/javac"

write_daml_home "$daml_install"
write_env_file "$java_home" "$daml_home_dir" "$daml_install"

"$repo_root/.venv/bin/python" -V >/dev/null 2>&1 || python3 -m venv "$venv_dir"
"$venv_dir/bin/python" -m pip install --upgrade pip >/dev/null
"$venv_dir/bin/python" -m pip install --requirement "$repo_root/requirements-cpl-validation.txt" >/dev/null

. "$runtime_dir/env.sh"
"$DAML_BIN" version >/dev/null
"$JAVA_HOME/bin/java" -version >/dev/null 2>&1

echo "bootstrap: Daml SDK $DAML_SDK_VERSION, Temurin JDK $JAVA_VERSION, and validation tooling are ready"
