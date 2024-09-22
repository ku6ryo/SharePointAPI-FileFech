import NextAuth from "next-auth"
import AzureProvider from "next-auth/providers/azure-ad"

const handler = NextAuth({
  providers: [
    AzureProvider({
      tenantId: process.env.AZURE_TENANT_ID,
      clientId: process.env.AZURE_CLIENT_ID!,
      clientSecret: process.env.AZURE_CLIENT_SECRET!,
      authorization: {
        params: {
          // need offline_access to get refresh token
          scope: 'openid profile Sites.Read.All offline_access',
        }
      }
    })
  ],
  callbacks: {
    signIn: async ({ user, account, profile, email, credentials }) => {
      console.log(user, account, profile, email, credentials)
      const accessToken = account?.access_token
      const r0 = await fetch('https://graph.microsoft.com/v1.0/sites?search=', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json;odata=verbose"
        },
      });
      console.log(await r0.text())
      console.log("##############\n\n")
      const r1 = await fetch('https://graph.microsoft.com/v1.0/sites/root/drives', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json;odata=verbose"
        },
      });
      console.log("R1", await r1.text())
      console.log("##############\n\n")
      const rd = await fetch('https://graph.microsoft.com/v1.0/sites/root/drives/b!kHwpKTT3Hk24BAxHOUDgIyorM3X0vV5Nod5xbZL1GulUzXWWA-OJQ64ZKwesPGT2', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json;odata=verbose"
        },
      });
      console.log("RD",await rd.text())
      console.log("##############\n\n")
      const rlist = await fetch('https://graph.microsoft.com/v1.0/sites/root/drives/b!kHwpKTT3Hk24BAxHOUDgIyorM3X0vV5Nod5xbZL1GulUzXWWA-OJQ64ZKwesPGT2/root/children', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json;odata=verbose"
        },
      });
      console.log("RLIST",await rlist.text())
      const rchild = await fetch('https://graph.microsoft.com/v1.0/sites/root/drives/b!kHwpKTT3Hk24BAxHOUDgIyorM3X0vV5Nod5xbZL1GulUzXWWA-OJQ64ZKwesPGT2/root/children/test/children', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json;odata=verbose"
        },
      });
      console.log("RCHILD",await rchild.text())
      console.log("##############\n\n")
      return true
    } 
  }
})

export { handler as GET, handler as POST }