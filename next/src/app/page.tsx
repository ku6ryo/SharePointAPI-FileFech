"use client"
import { signIn, signOut, } from "next-auth/react"

export default function Home() {
  return (
    <div>
      <div>
        <button onClick={() => signIn()}>Sign in</button>
      </div>
      <div>
        <button onClick={() => signOut()}>Sign out</button>
      </div>
    </div>
  )
}
