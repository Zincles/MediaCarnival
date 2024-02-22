<template>
    <div class="fullscreen bg-dark text-white text-center q-pa-md flex flex-center">
        <div>
            <div style="font-size: 30vh">404</div>
            <div class="text-h3">页面未找到</div>
            <q-separator class="q-mt-xl q-mb-xl" color="white" />
            <div class="text-h2" style="opacity: 0.4">这里什么也没有, 你大概是把什么给搞错了.</div>

            <q-btn
                class="q-mt-xl"
                color="grey-9"
                text-color="white"
                size="20px"
                unelevated
                to="/"
                label="返回主页"
                no-caps
            />
        </div>
    </div>
</template>

<script setup lang="ts"></script>
