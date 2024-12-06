import { mergeApplicationConfig, ApplicationConfig } from '@angular/core';
import { provideServerRendering } from '@angular/platform-server';
import { appConfig } from './app.config';

const serverConfig: ApplicationConfig = {
  providers: [
    provideServerRendering(),
    // Provide the base API URL for the server-side application
    {
      provide: 'BASE_API_URL',
      useValue: 'http://127.0.0.1:5000' // URL of your Flask backend
    }
  ]
};

// Merging the existing app configuration with the server configuration
export const config = mergeApplicationConfig(appConfig, serverConfig);