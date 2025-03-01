pkgname=amdgpu-fan
pkgdesc="Python daemon for controlling the fans on amdgpu cards"
pkgver=0.1.0
pkgrel=1
arch=('any')
license=('GPL2')
depends=('python' 'python-yaml' 'python-numpy')
makedepends=('python-setuptools')
url="https://github.com/zzkW35/amdgpu-fan"
source=("https://github.com/zzkW35/amdgpu-fan/archive/${pkgver}.tar.gz")
md5sums=('SKIP')

build() {
  cd "$srcdir/$pkgname-$pkgver"
  sed -i "s/PROJECTVERSION/$pkgver/g" setup.py
  python setup.py build
}

package() {
  cd "$srcdir/$pkgname-$pkgver"
  sed -i "s/PROJECTVERSION/$pkgver/g" setup.py
  python setup.py install --prefix=/usr --root="$pkgdir"
  mkdir -p "$pkgdir/usr/lib/systemd/system"
  install -Dm644 amdgpu-fan.service "$pkgdir/usr/lib/systemd/system/"
} 