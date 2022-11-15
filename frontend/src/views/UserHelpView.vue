<template>
    <header class="bg-white">
      <div class="flex flex-col md:flex-row md:items-center gap-4 md:gap-12">
        <RouterLink to="/" class="pl-4 md:pl-12 mx-auto lg:mx-0 p-2">
            <img alt="Vue logo" class="logo max-w-max h-20" src="@/assets/cropped-LOGO-GSO_neu.png" />
        </RouterLink>
        <div class="flex flex-row justify-center md:justify-start items-center gap-4 p-4 md:gap-12 md:h-24">
          <div><RouterLink to="/login">Einloggen</RouterLink></div>
          <div><RouterLink to="/register">Registrieren</RouterLink></div>
          <div><RouterLink to="/help">Benutzerhilfe</RouterLink></div>
        </div>
      </div>
    </header>
    <h1>Benutzerhilfe</h1>
</template>