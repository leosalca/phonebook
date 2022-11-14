
<script setup lang="ts">
import { defineComponent } from 'vue';
import { NList, NListItem, NThing, NAvatar, NIcon } from 'naive-ui';
import { PersonFilled } from '@vicons/material';

const msg = "hello world";

</script>

<template>
    <NList clickable hoverable>
        <NListItem>
            <NThing>
                <template #avatar>
                    <n-avatar>
                        <n-icon>
                            <PersonFilled />
                        </n-icon>
                    </n-avatar>
                </template>
            </NThing>
        </NListItem>
    </NList>
</template>