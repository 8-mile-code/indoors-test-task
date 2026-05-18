import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (request, next) => {
  if (request.url.includes('/auth/')) {
    return next(request);
  }

  const accessToken = localStorage.getItem('access_token');

  if (!accessToken) {
    return next(request);
  }

  const authRequest = request.clone({
    setHeaders: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  return next(authRequest);
};
