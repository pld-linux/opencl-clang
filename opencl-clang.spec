
# requires the OpenCL patches
%define llvm_version 11.0.0

%define spirv_llvm_translator_version 11.0.0

Summary:	Intel Graphics Compute Runtime for OpenCL
Name:		opencl-clang
Version:	11.0.0
Release:	4
License:	University of Illinois/NCSA Open Source License
Group:		Libraries
Source0:	https://github.com/intel/opencl-clang/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	31e0ca207e06d6bb1a49661cafd8a3ea
URL:		https://01.org/compute-runtime
BuildRequires:	SPIRV-LLVM-Translator-devel >= %{spirv_llvm_translator_version}
BuildRequires:	clang >= %{llvm_rpm_version}
BuildRequires:	clang-devel >= %{llvm_version}
BuildRequires:	cmake >= 3.4.3
BuildRequires:	llvm-devel >= %{llvm_version}
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Common clang is a thin wrapper library around clang. Common clang has
OpenCL-oriented API and is capable to compile OpenCL C kernels to
SPIR-V modules.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
%requires_eq	clang-devel
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -q

%build
install -d build
cd build
%cmake \
	-DUSE_PREBUILT_LLVM=ON \
	-DPREFERRED_LLVM_VERSION="%{llvm_version}" \
	-DLLVMSPIRV_INCLUDED_IN_LLVM=OFF \
	-DSPIRV_TRANSLATOR_DIR="%{_prefix}" \
	-DGIT_EXECUTABLE=/bin/false \
	../
%{__make}

cd ..

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_libdir}/libopencl-clang.so.11 $RPM_BUILD_ROOT%{_libdir}/libopencl-clang.so.%{llvm_version}
ln -s libopencl-clang.so.%{llvm_version} $RPM_BUILD_ROOT%{_libdir}/libopencl-clang.so.11
ln -sf libopencl-clang.so.%{llvm_version} $RPM_BUILD_ROOT%{_libdir}/libopencl-clang.so

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libopencl-clang.so.%{llvm_version}
%ghost %attr(755,root,root) %{_libdir}/libopencl-clang.so.11

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libopencl-clang.so
%{_includedir}/cclang
