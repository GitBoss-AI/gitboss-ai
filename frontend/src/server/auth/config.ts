import { type DefaultSession, type NextAuthConfig, type User } from "next-auth";
import CredentialProvider from "next-auth/providers/credentials";
import { env } from "@/env";
import * as bcrypt from "bcrypt";

/**
 * Module augmentation for `next-auth` types. Allows us to add custom properties to the `session`
 * object and keep type safety.
 *
 * @see https://next-auth.js.org/getting-started/typescript#module-augmentation
 */
declare module "next-auth" {
  interface Session extends DefaultSession {
    user: {
      id: string;
      // ...other properties
      // role: UserRole;
    } & DefaultSession["user"];
  }
  // interface User {
  //   // ...other properties
  //   // role: UserRole;
  // }
}

/**
 * Options for NextAuth.js used to configure adapters, providers, callbacks, etc.
 *
 * @see https://next-auth.js.org/configuration/options
 */
export const authConfig = {
  providers: [
    CredentialProvider({
      // `credentials` is used to generate a form on the sign in page.
      // You can specify which fields should be submitted, by adding keys to the `credentials` object.
      // e.g. domain, username, password, 2FA token, etc.
      // You can pass any HTML attribute to the <input> tag through the object.
      credentials: {
        email: { label: "Email", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        // Add logic here to look up the user from the credentials supplied
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        try {
          // Check if the provided password matches the hash in the environment
          const email = credentials.email as string;
          const password = credentials.password as string;

          const isValidPassword = await bcrypt.compare(
            password,
            env.AUTH_PASSWORD_HASH as string,
          );

          if (isValidPassword) {
            // Create a user object to return
            // Make sure this return type matches the NextAuth User type
            const user: User = {
              id: "admin-user",
              email: email,
              name: "Admin User",
            };
            return user;
          } else {
            return null;
          }
        } catch (error) {
          console.error("Authentication error:", error);
          return null;
        }
      },
    }),
    /**
     * ...add more providers here.
     *
     * Most other providers require a bit more work than the Discord provider. For example, the
     * GitHub provider requires you to add the `refresh_token_expires_in` field to the Account
     * model. Refer to the NextAuth.js docs for the provider you want to use. Example:
     *
     * @see https://next-auth.js.org/providers/github
     */
  ],
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // 30 days
    updateAge: 24 * 60 * 60, // 24 hours
  },
  callbacks: {
    session: ({ session, token, user }) => {
      if (token) {
        // For JWT strategy (credentials provider)
        return {
          ...session,
          user: {
            ...session.user,
            id: token.sub,
          },
        };
      }
      if (user) {
        // For database strategy (Google provider)
        return {
          ...session,
          user: {
            ...session.user,
            id: user.id,
          },
        };
      }
      return session;
    },
    jwt: ({ token, user }) => {
      if (user) {
        token.id = user.id;
      }
      return token;
    },
    async redirect({ baseUrl }) {
      return `${baseUrl}`;
    },
  },
  // theme: {
  //   logo: `${env.URL}/logo.png`,
  // },
  trustHost: true,
} satisfies NextAuthConfig;
