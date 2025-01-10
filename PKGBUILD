# Maintainer: littzhch <2371050115@qq.com>
pkgname=clash-multi-conf
pkgver=0.1.0
pkgrel=1
epoch=
pkgdesc="A simple clash wrapper to manage multiple clash config files"
arch=('any')
url=""
license=('GPL')
groups=()
depends=('clash' 'python-deepmerge' 'python-yaml')
makedepends=()
checkdepends=()
optdepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=()
install=
changelog=
source=("clash-multi-conf.py" "clash-multi-conf.service")
noextract=()
sha256sums=('SKIP' 'SKIP')
validpgpkeys=()

package() {
	install -Dm755 clash-multi-conf.py "$pkgdir/usr/bin/clash-multi-conf"
	install -Dm644 clash-multi-conf.service "$pkgdir/usr/lib/systemd/user/clash-multi-conf.service"
}
